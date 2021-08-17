//
// Created by liors on 03-Jun-21.
//

#include "Barrier.h"
#include "MapReduceFramework.h"
#include "MapReduceClient.h"
#include <pthread.h>
#include <atomic>
#include <iostream>
#include <algorithm>
#include <vector>

#define SYSTEM_ERROR "system error: "
#define FINISHED_ATOMIC 31
#define HEXA 0x7fffffff
#define STAGE_SHIFT 62u
#define MAP 1ULL
#define SHUFFLE 2ULL
#define REDUCE_ 3ULL
#define PERCENT 100
#define MUT_ERR "pthread mutex error"
#define TH_ERR "pthread error"

using namespace std;
struct JobContext;

/**
 * prints the error message with the given one and exit the program with exit code
 * @param s the attached error message to print
 */
inline void systemError(string const& s)
{
    cerr << SYSTEM_ERROR << s << endl;
    exit(1);
}

/**
 * a class for each thread context with its own id, vector of mapped pairs and a shared pointer to the main struct
 */
class ThreadContext {
public:
    const int id;
    JobContext* context;
    IntermediateVec *mapOutQueues;

    ThreadContext(const int id, JobContext *context) :
            id(id), context(context) {
        mapOutQueues = new IntermediateVec;
    }
};

/**
 * the main struct of the job
 */
struct JobContext {
    stage_t stage = UNDEFINED_STAGE; // the current stage of the job
    const MapReduceClient* client; // a pointer to the client with its map and reduce functions
    pthread_t *JobThreads;  // list of pthreads
    int multiThreadLevel; // the number of pthreads the execute the job with
    pthread_mutex_t *JobMutex; // saves the outputVec from mutual exclusion
    pthread_mutex_t* WaitMutex; // saves the pthread_join to be called twice in same progress
    ThreadContext** thread_contexts; // the list of threads contexts
    const InputVec* inputVec; // the given input vector
    OutputVec* outputVec; // the given address of the output vector
    IntermediateVec *mapOfAll; // unionised of all the mapped pairs from all the threads
    vector <IntermediateVec*> *shuffle; // the outcome of the shuffle stage
    Barrier barrier; // barrier as been given in the resource files
    bool wait; // a flag to which the waitForJob function as been called already
    long input_size; // the size of the given input vector
    unsigned long long pairs_num = 0; // the number of all the pairs that have been made
    JobState* curr_state; // struct of the job state
    /**
     * atomic counter that holds information (left to right) according to the current stage
     * 2 bits - the stage of the job
     * 31 bits - the number of the inputs we started to work on
     * 31 bits - the number of the inputs we finished to work on
     */
    atomic<uint64_t>* atomic_counter;

    // job struct constructor
    JobContext(const MapReduceClient *client, int threadCount, const InputVec &inputVec,
               OutputVec &outputVec) :
            client(client), multiThreadLevel(threadCount), inputVec(&inputVec), outputVec(&outputVec), barrier(threadCount), wait(false){
        input_size = inputVec.size();
        JobThreads = new (std::nothrow)pthread_t[threadCount];
        JobMutex = new (std::nothrow)pthread_mutex_t;
        if(pthread_mutex_init(JobMutex, nullptr) != 0){
            systemError(MUT_ERR);
        }
        WaitMutex = new (std::nothrow)pthread_mutex_t;
        if(pthread_mutex_init(WaitMutex, nullptr) != 0){
            systemError(MUT_ERR);
        }
        thread_contexts = new (std::nothrow) ThreadContext*[threadCount];
        mapOfAll = new vector<IntermediatePair>;
        shuffle = new vector<IntermediateVec *>;
        curr_state = new (std::nothrow) JobState();
        curr_state->percentage = 0;
        curr_state->stage = UNDEFINED_STAGE;
        atomic_counter = new (std::nothrow) atomic<uint64_t>(0);
    }
    // job struct destructor
    ~JobContext() {
        delete [] JobThreads;
        pthread_mutex_destroy(JobMutex);
        delete JobMutex;
        delete mapOfAll;
        delete curr_state;
        for(auto& vec : *shuffle){
            delete vec;
        }
        delete shuffle;
        delete atomic_counter;
        pthread_mutex_destroy(WaitMutex);
        delete WaitMutex;
        for (int i = 0; i < multiThreadLevel; i++) {
            delete thread_contexts[i]->mapOutQueues;
            delete thread_contexts[i];
        }
        delete [] thread_contexts;
    }

};

/**
 * return the current stage from the atomic counter
 * @param counter unsigned long long -> atomic counter.load
 * @return the stage
 */
//enum stage_t {UNDEFINED_STAGE=0, MAP_STAGE=1, SHUFFLE_STAGE=2, REDUCE_STAGE=3};
inline stage_t getStage(unsigned long long counter){
    return (stage_t)(counter >> 62u);
}

/**
 * return the number of the finished threads - map/shuffle/reduce
 * @param counter unsigned long long -> atomic counter.load
 * @return only the part that counts the finished in the atomic counter
 */
inline unsigned long long numFinished(unsigned long long counter)
{
    return (unsigned long long) ((counter >> FINISHED_ATOMIC) & (HEXA));
}

/**
 * The function receives as input intermediary element (K2, V2) and context which contains
 * data structure of the thread that created the intermediary element. The function saves the
 * intermediary element in the context data structures. In addition, the function updates the
 * number of intermediary elements using atomic counter.
 * Please pay attention that emit2 is called from the client's map function and the context is
 * passed from the framework to the client's map function as parameter.
 * @param key given key
 * @param value given value
 * @param context ThreadContext instance
 */
void emit2(K2 *key, V2 *value, void *context)
{
    auto* job = (ThreadContext*) context;
    IntermediatePair pair(key, value);
    job->mapOutQueues->push_back(pair);
}
/**
 * The function receives as input output element (K3, V3) and context which contains data
 * structure of the thread that created the output element. The function saves the output
 * element in the context data structures (output vector). In addition, the function updates the
 * number of output elements using atomic counter.
 * Please pay attention that emit3 is called from the client's map function and the context is
 * passed from the framework to the client's map function as parameter.
 * @param key  given key
 * @param value given value
 * @param context JobContext struct
 */
void emit3 (K3* key, V3* value, void* context)
{
    auto* job = (JobContext*) context;
    OutputPair my_pair(key, value);
    // protect from mutual exclusion when different threads try to reach the output vector
    if (pthread_mutex_lock(job->JobMutex) != 0){
        systemError(MUT_ERR);
    }
    (*job->outputVec).push_back(my_pair);
    if(pthread_mutex_unlock(job->JobMutex) != 0)
    {
        systemError(MUT_ERR);
    }
}

/**
 * shuffle all the pairs from the different threads that have been made in map stage
 * @param job pointer for JobContext struct
 */
void shuffleIt(JobContext* job)
{
    auto key = job->mapOfAll->back().first;
    while(!(job->mapOfAll->empty())) {
        IntermediateVec* keyVec = new (std::nothrow) IntermediateVec;
        while (!(job->mapOfAll->empty()) && !((*key) < *job->mapOfAll->back().first) && !(*job->mapOfAll->back().first < *key)) {
            (*job->atomic_counter).fetch_add(1); // increase started
            (*keyVec).push_back((*job->mapOfAll).back());
            (*job->atomic_counter).fetch_add((1ULL << 31u)); // increase finished
            (*job->mapOfAll).pop_back();
        }
        if (!(*job->mapOfAll).empty()){
            key = job->mapOfAll->back().first;
        }
        (*job->shuffle).push_back(keyVec);
    }
}

/**
 * comparator for the sort phase
 * @param p1 pair
 * @param p2 pair
 * @return true if the key of the first pair is smaller than the seconds pair key. false otherwise
 */
bool comp(IntermediatePair& p1, IntermediatePair& p2)
{
    return *(p1.first) < *(p2.first);
}

/**
 * create and call the client reduce
 * @param job pointer for the job struct
 */
void doReduce(JobContext* job){
    unsigned long long i;
    unsigned long long suff_size = (*job->shuffle).size();
    while((i = (*(job->atomic_counter)).fetch_add(1) & (HEXA)) < suff_size) {
        if (i < suff_size) {
            job->client->reduce((*job->shuffle)[i], job);
            (*job->atomic_counter).fetch_add((unsigned long long)(((*(*job->shuffle)[i]).size())<< FINISHED_ATOMIC));
        }
    }
}

/**
 * the function that starts the progress of each pthread
 * @param arg pointer to threadContext
 * @return nullptr
 */
void *startJob(void* arg)
{
    auto* thread = (ThreadContext*) arg;
    auto *job = thread->context;
    // map stage
    if (getStage((*job->atomic_counter).load()) != MAP_STAGE){
        (*job->atomic_counter).fetch_add(MAP << STAGE_SHIFT);
        job->stage = MAP_STAGE;
    }
    unsigned long long i;
    while((i = ((*job->atomic_counter).fetch_add(1) & (HEXA))) < (unsigned long long)job->input_size) {
        job->client->map((*(job->inputVec))[i].first, (*(job->inputVec))[i].second, thread);
        (*job->atomic_counter).fetch_add(MAP << 31u);
    }
    // sort the pairs vector
    std::sort(thread->mapOutQueues->begin(), thread->mapOutQueues->end(), comp);
    // a barrier in order to prevent any thread from continuing before all the threads finished map stage
    job->barrier.barrier();
    if(thread->id == 0)
    {
        // combine all the pairs from the different threads vectors into one sorted vector
        for(int j = 0; j < job->multiThreadLevel; j++){
            job->pairs_num += (*job->thread_contexts[j]->mapOutQueues).size();
            while(!(job->thread_contexts[j]->mapOutQueues->empty())){
                job->mapOfAll->push_back(job->thread_contexts[j]->mapOutQueues->back());
                job->thread_contexts[j]->mapOutQueues->pop_back();
            }
        }
        std::sort(job->mapOfAll->begin(), job->mapOfAll->end(), comp);
        // shuffle stage
        job->atomic_counter->store(SHUFFLE << STAGE_SHIFT);
        job->stage = SHUFFLE_STAGE;
        shuffleIt(job);
        // reduce stage
        job->atomic_counter->store(REDUCE_ << STAGE_SHIFT);
        job->stage= REDUCE_STAGE;
    }
    // barrier in order to prevent any thread from continuing before the 0 thread finished the shuffle stage
    job->barrier.barrier();
    doReduce(job);
    return nullptr;
}

/**
 * @param client The implementation of MapReduceClient or in other words the task that the
    framework should run.
 * @param inputVec a vector of type std::vector<std::pair<K1*, V1*>>, the input elements
 * @param outputVec a vector of type std::vector<std::pair<K3*, V3*>>, to which the output
 * elements will be added before returning. You can assume that outputVec is empty.
 * @param multiThreadLevel number of worker threads to be used for running the algorithm.
 * You will have to create threads using c function pthread_create. You can assume
 * multiThreadLevel argument is valid (greater or equal to 1).
 * @return - The function returns JobHandle that will be used for monitoring the job.
 */
JobHandle startMapReduceJob(const MapReduceClient &client, const InputVec &inputVec, OutputVec &outputVec, int multiThreadLevel)
{
    JobContext *handle = new JobContext(&client, multiThreadLevel, inputVec, outputVec);
    int res;
    // creates a thread context class for each pthread
    ThreadContext* thread_context;
    for (int i = 0; i < multiThreadLevel; ++i) {
        thread_context = new (std::nothrow) ThreadContext(i, handle);
        handle->thread_contexts[i] = thread_context;
    }
    // creates multiThreadLevel number of pthreads, each one of them will call startJob
    for(int counter = 0; counter < multiThreadLevel; counter++)
    {
        res = pthread_create(&(handle->JobThreads[counter]), nullptr, startJob, handle->thread_contexts[counter]);
        if (res != 0)
        {
            systemError(TH_ERR);
        }
    }
    return (static_cast<JobHandle> (handle));
}

//----------------------------------- client functions -----------------------------------------------

/**
 * a function gets JobHandle returned by startMapReduceFramework and waits until it is finished.
 * @param job
 * you should use the c function pthread_join.It is legal to call the function more than once and
 * you should handle it. Pay attention that calling pthread_join twice from the same process has
 * undefined behavior and you must
 * avoid that.
 */
void waitForJob(JobHandle job)
{
    JobContext* context = static_cast<JobContext *>(job);
    // the mutex make a thread wait, if another thread called this function before
    if (pthread_mutex_lock(context->WaitMutex) != 0){
        systemError(MUT_ERR);
    }
    // the pthread_join can be called only once in a process
    if (!context->wait)
    {
        context->wait = true;
        for(int counter = 0; counter < context->multiThreadLevel; counter++)
        {
            if(pthread_join(context->JobThreads[counter], nullptr) != 0)
            {
                systemError(TH_ERR);
            }
        }
    }
    if (pthread_mutex_unlock(context->WaitMutex) != 0){
        systemError(MUT_ERR);
    }
}

/**
 * this function gets a JobHandle and updates the stage of the job into the given JobState struct.
 * @param job
 * @param state
 */
void getJobState(JobHandle job, JobState *state)
{
    JobContext* context = (JobContext *)job;
    unsigned long long counter = (*context->atomic_counter).load();
    // set the current stage
    state->stage = getStage(counter);
    auto finished = (float) numFinished(counter);
    // set the current percentage
    if (state->stage == UNDEFINED_STAGE){
        state->percentage = 0;
    }
    else if (state->stage == MAP_STAGE){
        float percentage = (finished /(float)(context->input_size)) * PERCENT;
        state->percentage = percentage;
        context->curr_state->percentage = percentage;
    }
    else{
        float percentage2 = (finished /(float)(context->pairs_num)) * PERCENT;
        state->percentage = percentage2;
        context->curr_state->percentage = percentage2;
    }
}

/**
 * Releasing all resources of a job. You should prevent releasing resources
 * before the job finished. After this function is called the job handle will be invalid.
 * @param job
 */
void closeJobHandle(JobHandle job)
{
    auto* context = (JobContext *)job;
    // waits the job to be done before deleting all and turning off the lights
    waitForJob(job);
    delete context;
    job = nullptr;
}