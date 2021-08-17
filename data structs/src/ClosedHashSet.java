/**
 * A class of closed hash set implementing SimpleHashSet
 */
public class ClosedHashSet extends SimpleHashSet{
    /**
     * return value when object not found
     */
    final private int NOT_FOUND = -1;
    /**
     * the hashtable containing the strings
     */
    private Tuple[] table = new Tuple[this.currentCapacity];

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25)
     */
    public ClosedHashSet(){
        super();
    }

    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     * @param upperLoadFactor - The upper load factor of the hash table.
     * @param lowerLoadFactor - The lower load factor of the hash table.
     */
    public ClosedHashSet(float upperLoadFactor,
                       float lowerLoadFactor){
        super(upperLoadFactor, lowerLoadFactor);

    }

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25)
     * @param data - Values to add to the set.
     */
    public ClosedHashSet(String[] data){
        this();
        for (String str: data)
            this.add(str);
    }
    /**
     * @return The current capacity (number of cells) of the table.
     */
    public int capacity(){
        return this.currentCapacity;
    }
    /**
     * Add a specified element to the set if it's not already in it.
     * @param newValue New value to add to the set
     * @return False if newValue already exists in the set
     */
    public boolean add(String newValue){
        if (this.contains(newValue))
            return false;
        float loadFactor = (float)(this.size()+1)/(this.capacity());
        if (loadFactor > this.getUpperLoadFactor()){
            this.currentCapacity = this.capacity()*2;
            this.rehashTable();
        }
        int hashCode = newValue.hashCode();
        int index;
        for (int i = 0; i < this.capacity(); i++) {
            index = this.clamp(this.probing(i, hashCode));
            if (this.table[index] == null){
                this.table[index]= new Tuple(newValue);
                this.objCounter++;
                return true;
            }
            if(this.table[index].isDeleted()){
                this.table[index]=new Tuple(newValue);
                this.objCounter++;
                return true;
            }
        }
        return false;
    }

    /**
     * @param i index for the probing calculation
     * @param hash the string hashcode
     * @return the probing calculation
     */
    private int probing(int i, int hash){
        return (hash +(i+i*i)/2);
    }

    /**
     * Look for a specified value in the set.
     * @param searchVal Value to search for
     * @return True iff searchVal is found in the set
     */
    public boolean contains(String searchVal) {
        int index = isContains(searchVal);
        if (index != NOT_FOUND )
            return !this.table[index].isDeleted();
        return false;
    }

    /**
     * @param searchVal Value to search for
     * @return the index of the object in the hashtable or -1 if not found
     */
    private int isContains(String searchVal){
        int hashCode = searchVal.hashCode();
        int index;
        for (int i = 0; i < this.capacity(); i++) {
            index = this.clamp(this.probing(i, hashCode));
            if (this.table[index] == null)
                return NOT_FOUND;
            if(this.table[index].equals(searchVal))
                return index;
        }
        return NOT_FOUND;
    }
    /**
     * rehashing the elements to a new table that will comply the load factor
     */
    private void rehashTable() {
        this.objCounter = 0;
        Tuple[] oldTable = this.table;
        this.table = new Tuple[this.currentCapacity];
        for (Tuple tuple: oldTable){
            if(tuple != null)
                if(!tuple.isDeleted())
                    this.add(tuple.string);
        }
    }

    /**
     * Remove the input element from the set.
     * @param toDelete Value to delete
     * @return True if toDelete is found and deleted
     */
    public boolean delete(String toDelete){
        int index = isContains(toDelete);
        if(index != NOT_FOUND){
            if(!this.table[index].isDeleted()) {
                this.table[index].Delete();
                this.objCounter--;
                float loadFactor = (float)(this.size())/(this.capacity());
                if (loadFactor<this.getLowerLoadFactor() && this.capacity() > 1){
                    this.currentCapacity = this.capacity() / 2;
                    this.rehashTable();
                }
                return true;
            }
        }
        return false;
    }
}
