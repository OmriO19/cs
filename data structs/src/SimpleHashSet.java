/**
 * A superclass for implementations of hash-sets implementing the SimpleSet interface.
 */
public abstract class SimpleHashSet implements SimpleSet {

    /**
     * Describes the higher load factor of a newly created hash set
     */
    protected static final float DEFAULT_HIGHER_CAPACITY = 0.75f;
    private float upperCapacity;

    /**
     * Describes the lower load factor of a newly created hash set
     */
    protected static final float DEFAULT_LOWER_CAPACITY = 0.25f;
    private float lowerCapacity;

    /**
     * Describes the capacity of a newly created hash set
     */
    protected static final int INITIAL_CAPACITY = 16;

    /**
     * the current capacity of the hash set
     */
    protected int currentCapacity;
    /**
     * the number of objects in the hash set
     */
    protected int objCounter;

    /**
     * Constructs a new hash set with the default capacities given in DEFAULT_LOWER_CAPACITY and
     * DEFAULT_HIGHER_CAPACITY
     */
    protected SimpleHashSet(){
        this.currentCapacity = INITIAL_CAPACITY;
        this.upperCapacity = DEFAULT_HIGHER_CAPACITY;
        this.lowerCapacity = DEFAULT_LOWER_CAPACITY;
    }

    /**
     * Constructs a new hash set with capacity INITIAL_CAPACITY
     * @param upperLoadFactor - the upper load factor before rehashing
     * @param lowerLoadFactor - the lower load factor before rehashing
     */
    protected SimpleHashSet(float upperLoadFactor,
                            float lowerLoadFactor){
        this.currentCapacity = INITIAL_CAPACITY;
        this.upperCapacity = upperLoadFactor;
        this.lowerCapacity = lowerLoadFactor;
    }

    /**
     * @return The current capacity (number of cells) of the table.
     */
    public abstract int capacity();

    /**
     * Clamps hashing indices to fit within the current table capacity (see the exercise description for
     * details)
     * @param index - the index before clamping
     * @return an index properly clamped
     */
    protected int clamp(int index){
        return index & (this.currentCapacity -1);
    }

    /**
     * @return The lower load factor of the table.
     */
    protected float getLowerLoadFactor(){
        return this.lowerCapacity;
    }

    /**
     * @return The higher load factor of the table.
     */
    protected float getUpperLoadFactor(){
        return this.upperCapacity;
    }

////////////////

    /**
     * Add a specified element to the set if it's not already in it.
     * @param newValue New value to add to the set
     * @return False if newValue already exists in the set
     */
    public abstract boolean add(String newValue);

    /**
     * Look for a specified value in the set.
     * @param searchVal Value to search for
     * @return True if searchVal is found in the set
     */
    public abstract boolean contains(String searchVal);
    /**
     * Remove the input element from the set.
     * @param toDelete Value to delete
     * @return True if toDelete is found and deleted
     */
    public abstract boolean delete(String toDelete);
    /**
     * @return The number of elements currently in the set
     */
    public int size(){
        return objCounter;
    }
}
