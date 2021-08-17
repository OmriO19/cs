#include "VirtualMemory.h"
#include "PhysicalMemory.h"

#define FAILURE 0;
#define SUCCESS 1;

/**
 * Clears a frame before running
 * @param frameIndex
 */
void clearTable(uint64_t frameIndex)
{
    for (uint64_t i = 0; i < PAGE_SIZE; ++i)
    {
        PMwrite(frameIndex * PAGE_SIZE + i, 0);
    }
}

/**
 * Initialize the root frame
 */
void VMinitialize()
{
    clearTable(0);
}


/**
 * calculate the weight of the current page in the recursion path
 * @param value current page value
 * @return WEIGHT_EVEN if the value is even WEIGHT_ODD else
 */
int calculateWeight(uint64_t value)
{
    if (value % 2 == 0)
    {
        return WEIGHT_EVEN;
    }
    else
    {
        return WEIGHT_ODD;
    }
}

/**
 * checks if we are in the case where the two weights are equal,  if so we will pick page with the
 * smallest number to be evacuated
 * @param max_weight the current max weight in the recursion
 * @param max_page the page that holds the max weight in the recursion
 * @param weight weight we got in the new recursion
 * @param curPageNumber page we got in the new recursion
 * @return
 */
bool is_equal_weight(int &max_weight, uint64_t &max_page, int weight, uint64_t &curPageNumber)
{
    return (weight == max_weight && curPageNumber < max_page);
}

/**
 * this function do the eviction
 * @param frame frame to be evicted
 * @return the frame we evicted
 */
uint64_t evictMaxWeight(uint64_t frame);

/**
 * checks if the frame is empty
 * @param inPath frame in the current path that cant be empty
 * @param currFrame frame we are checking in this cycle of the recursion (has to be not 0 or the
 * inPath frame
 * @param depth the current depth of the recursion (has to be  < TABLES_DEPTH)
 * @return true if empty, false otherwise
 */
bool isEmptyFrame(uint64_t inPath, uint64_t currFrame, int depth);

/**
 * this function reset a frame -> filling it with zeros
 */
void resetFrame(uint64_t physicalAddress)
{
    PMwrite(physicalAddress, 0);
}

uint64_t dfs(int &maxWeight, uint64_t &maxFrame, uint64_t pageIndex, uint64_t currPage, uint64_t currFrame,
    uint64_t inPath, int depth, int weight, uint64_t &toEvict);

/**
 * main function! calls traverse and dfs and evicts frames if neccecery
 * traversing throw the frames to get the frame that holds the page we got from the DFS
 * @param currFrameAddress address of the current frame we are looking at
 * @param prevFrame address of the frame in the table (initialize with 0)
 * @param page page index from the currFrameAddress
 * @param offset current offset width
 * @param currOffset the rest of the offset
 * @param toEvict flag that represent if we need to evict or not
 * @return relevant frame
 */
uint64_t
traverse(uint64_t currFrameAddress, uint64_t prevFrame, uint64_t page, int offset,
         int currOffset, bool toEvict)
{
    word_t value;
    // get the physical address from the page
    uint64_t of = currOffset - offset;
    uint64_t shiftPage = page >> of;
    //go back to the prev page
    uint64_t prevIndex = shiftPage << of;
    uint64_t physical = prevFrame + shiftPage;

    //terminate condition
    if (currOffset == 0)
    {
        return prevFrame;
    }
    //read what in the frame
    PMread(physical, &value);
    //if not empty
    if (value != 0)
    {
        //need to be evicted and therefore reset the frame
        bool toRestore (currOffset == offset);
        if (toRestore && toEvict)
        {
            resetFrame(physical);
        }
        //call recursion of the traverse function in order to return the frame that relevant to th page we got
        auto currPage = ((prevIndex & ~page) | (page & ~prevIndex));
        auto updateOffset = currOffset - offset;
        return traverse(currFrameAddress, value * PAGE_SIZE, currPage, OFFSET_WIDTH,
                        updateOffset, toEvict);
    }
    //if the value we read is empty
    //objects we will want to save from the dfs
    int max_weight = 0;
    uint64_t evict = currFrameAddress;
    uint64_t maxFrame = 0;
    //run the dfs to find the next frame
    uint64_t nextFrame = dfs(max_weight, maxFrame, currFrameAddress, 0, 0,
                             prevFrame, 0, 0, evict);
    //address to restore
    auto restore = nextFrame / PAGE_SIZE;
    bool toRestore (currOffset == offset);
    if (!toRestore)
    {
        //if not so clear the address
        clearTable(restore);
    }
    else
    {
        PMrestore(restore, currFrameAddress);
    }

    //write to the prev address the restore value
    uint64_t writeAddress = prevFrame + shiftPage;
    PMwrite(writeAddress, restore);
    auto currPage = ((prevIndex & ~page) | (page & ~prevIndex));
    auto updateOffset = currOffset - offset;
    //return the frame we traverse
    return traverse(currFrameAddress, nextFrame, currPage, OFFSET_WIDTH,
                    updateOffset, toEvict);
}

/**
 * the program DFS on the table tree
 * @param maxWeight the current max weight (initialize with 0)
 * @param maxFrame the current max frame (initialize with 0)
 * @param pageIndex index of the current page we are in
 * @param currPage the current page we got to in the recursion (initialize with 0)
 * @param currFrame the current frame address we got to in the recursion (initialize with 0)
 * @param inPath page in the path of the recursion and therefore cant be evicted
 * @param depth the current depth we got to in the recursion (initialize with 0)
 * @param weight the current weight we got to in the recursion (initialize with 0)
 * @param toEvict the frame we will evict
 * @return
 */
uint64_t
dfs(int &maxWeight, uint64_t &maxFrame, uint64_t pageIndex, uint64_t currPage, uint64_t currFrame,
    uint64_t inPath, int depth, int weight, uint64_t &toEvict)
{
    // case 1 we have to remove the reference to this table from its parent.
    if (maxFrame < currFrame)
    {
        maxFrame = currFrame;
    }

    //const frame limit
    auto frameSize = NUM_FRAMES * PAGE_SIZE;
    word_t readValue;
    //when we get to a page we stop the recursion
    if (depth == TABLES_DEPTH)
    {
        //move page 1 offset
        currPage = currPage >> OFFSET_WIDTH;
        //update the weight
        weight += calculateWeight(currPage);
        //case 3 if we need to update the page we will evacuate
        if (is_equal_weight(maxWeight, toEvict, weight, currPage) || maxWeight < weight)
        {
            maxWeight = weight;
            toEvict = currPage;
        }
//        weight = 0;
        return FAILURE;
    }
    // the dfs part to go in the table path
    for (uint64_t i = 0; i < PAGE_SIZE; ++i)
    {
        //first read what in the frame
        auto read = currFrame + i;
        PMread(read, &readValue);
        if (readValue != 0)
        {
            //update the all the things for the recursion (weight, path == frame and page, depth)
            weight += calculateWeight(readValue);
            auto updatePage = (currPage + i) << OFFSET_WIDTH;
            int recursiveDepth = depth + 1;
            auto updateFrame = readValue * PAGE_SIZE;
            //call the recursion
            uint64_t currRecursivePath = dfs(maxWeight, maxFrame, pageIndex, updatePage,
                                             updateFrame,
                                             inPath, recursiveDepth, weight, toEvict);
            //update the weight back to its previous
            weight -= calculateWeight(readValue);
            //in case the value of the frame is no 0 (not empty) we will reset the frame with zeros
            if (currRecursivePath != 0)
            {
                if (currRecursivePath == (unsigned long long) updateFrame)
                {
                    auto physicalReset = currFrame + i;
                    resetFrame(physicalReset);
                }
                return currRecursivePath;
            }
        }
    }
    //if there is an empty frame return this frame  as available
    if (isEmptyFrame(inPath, currFrame, depth))
    {
        return currFrame;
    }


    //for the special case the depth is 0 -> only root we will evict the page with the max weight
    if (depth == 0)
    {
        //just if the max frame if bigger then the maximum of the whole table size == frameSize
        // if max_frame_index+1 < NUM_FRAMES then we know that the frame in the index (max_frame + 1) is unused.
        auto max = maxFrame + PAGE_SIZE;
        if (max >= (unsigned long long) frameSize)
        {
            //return the evicted frame
            return evictMaxWeight(toEvict);
        }
        return max;
    }
    //should not get here in any case.
    return FAILURE;
}

/**
 * checks if the current frame is empty -> fill with zeros
 * @param frame the current frame address
 * @return true if the frame is empty (0) and false otherwise
 */
bool isFillZero(uint64_t frame)
{
    word_t readValue;
    for (int i = 0; i < PAGE_SIZE; ++i)
    {
        auto physical = frame + i;
        PMread(physical, &readValue);
        if (readValue != 0)
        {
            return false;
        }
    }
    return true;
}

/**
 * checks if the frame is empty
 * @param inPath frame in the current path that cant be empty
 * @param currFrame frame we are checking in this cycle of the recursion (has to be not 0 or the
 * inPath frame
 * @param depth the current depth of the recursion (has to be  < TABLES_DEPTH)
 * @return true if empty, false otherwise
 */
bool isEmptyFrame(uint64_t inPath, uint64_t currFrame, int depth)
{
    //all the cases that have to be true in order for the frame to be empty
    return (isFillZero(currFrame) && currFrame != inPath && currFrame != 0 && depth < TABLES_DEPTH);
}


uint64_t evictMaxWeight(uint64_t frame)
{
    //starts with given frame as currFrameAddress and page, (VIRTUAL_ADDRESS_WIDTH - (TABLES_DEPTH * OFFSET_WIDTH) as page
    // VIRTUAL_ADDRESS_WIDTH - OFFSET_WIDTH as currOffset and true to evict
    uint64_t address = traverse(frame, 0, frame,
                                (VIRTUAL_ADDRESS_WIDTH - (TABLES_DEPTH * OFFSET_WIDTH)),
                                VIRTUAL_ADDRESS_WIDTH - OFFSET_WIDTH, true);
    //evict function
    PMevict((address / PAGE_SIZE), frame);
    return address;
}

/**
 *take from the virtualAddress only the offset
 * @param virtualAddress virtualAddress we got
 * @param offset the offset we took from it
 */
void findOffset(uint64_t virtualAddress, uint64_t *offset)
{
    auto page = virtualAddress >> (unsigned long long) OFFSET_WIDTH;
    auto notPage = ~(page << (unsigned long long) OFFSET_WIDTH);
    //calculate only the offset from the virtualAddress
    *offset = notPage & virtualAddress;
}

/**
 * reads / writes the word from the virtual address virtualAddress into value.
 * @param virtualAddress given virtual address
 * @param value value to write
 * @param valueRead value to read
 * @param read flag if read state
 * @return 1 on success and 0 on failure.
 */
int readOrWrite(uint64_t virtualAddress, word_t value, word_t *valueRead, bool read)
{
    //if that case the reading or writing should fail
    if (virtualAddress > VIRTUAL_MEMORY_SIZE -1)
    {
        return FAILURE;
    }

    //get the offset
    uint64_t offset;
    findOffset(virtualAddress, &offset);
    //get the frame address from the page
    //starts with virtualAddress >> OFFSET_WIDTH for frame and page
    //(VIRTUAL_ADDRESS_WIDTH - (TABLES_DEPTH * OFFSET_WIDTH)) as offset and dont evict
    uint64_t address = traverse(virtualAddress >> OFFSET_WIDTH, 0, virtualAddress >> OFFSET_WIDTH,
                                (VIRTUAL_ADDRESS_WIDTH - (TABLES_DEPTH * OFFSET_WIDTH)),
                                VIRTUAL_ADDRESS_WIDTH - OFFSET_WIDTH, false);
    if (read)
    {
        //read the physical address == address from the page translates to frame + offset
        PMread(address + offset, valueRead);
        return SUCCESS;
    }
    //write the physical address == address from the page translates to frame + offset
    PMwrite(address + offset, value);
    return SUCCESS;
}

/**
 * reads the word from the virtual address virtualAddress into *value.
 * @param virtualAddress
 * @param value
 * @return 1 on success and 0 on failure.
 */
int VMread(uint64_t virtualAddress, word_t *value)
{
    return readOrWrite(virtualAddress, 0, value, true);
}

/**
 * writes the word from the virtual address virtualAddress into *value.
 * @param virtualAddress
 * @param value
 * @return 1 on success and 0 on failure.
 */
int VMwrite(uint64_t virtualAddress, word_t value)
{
    return readOrWrite(virtualAddress, value, nullptr, false);
}