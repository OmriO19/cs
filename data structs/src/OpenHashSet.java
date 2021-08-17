import java.util.Iterator;

public class OpenHashSet extends SimpleHashSet {
    /**
     * the hash table of the open hash set
     */
    private ListLinked[] table = new ListLinked[this.currentCapacity];

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25)
     */
    public OpenHashSet(){
        super();
        for (int i = 0; i < this.currentCapacity; i++) {
            this.table[i] = new ListLinked();
        }
    }

    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     * @param upperLoadFactor - The upper load factor of the hash table.
     * @param lowerLoadFactor - The lower load factor of the hash table.
     */
    public OpenHashSet(float upperLoadFactor,
                       float lowerLoadFactor){
        super(upperLoadFactor, lowerLoadFactor);
        for (int i = 0; i < this.currentCapacity; i++) {
            this.table[i] = new ListLinked();
        }
    }

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25)
     * @param data - Values to add to the set.
     */
    public OpenHashSet(String[] data){
        this();
        for (String str: data)
            this.add(str);
    }

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
        float loadFactor = (float)(this.size() +1)/(this.capacity());
        if (loadFactor > this.getUpperLoadFactor()){
            this.currentCapacity = this.capacity()*2;
            this.rehashTable();
        }
        int hashCode = newValue.hashCode();
        this.table[this.clamp(hashCode)].add(newValue);
        this.objCounter++;
        return true;
    }

    /**
     * Look for a specified value in the set.
     * @param searchVal Value to search for
     * @return True iff searchVal is found in the set
     */
    public boolean contains(String searchVal) {
        int hashCode = searchVal.hashCode();
        int index = this.clamp(hashCode);
        return this.table[index].contains(searchVal);
    }

    /**
     * rehashing the elements to a new table that will comply the load factor
     */
    private void rehashTable() {
        this.objCounter = 0;
        ListLinked[] oldTable = this.table;
        this.table = new ListLinked[this.currentCapacity];
        for (int i = 0; i < this.currentCapacity; i++) {
            this.table[i] = new ListLinked();
        }
        for (ListLinked linkedList: oldTable){
            Iterator<String> it = linkedList.iterator();
            while (it.hasNext())
                this.add(it.next());
        }
    }

    /**
     * Remove the input element from the set.
     * @param toDelete Value to delete
     * @return True if toDelete is found and deleted
     */
    public boolean delete(String toDelete){
        int hashCode = toDelete.hashCode();
        if(this.table[this.clamp(hashCode)].delete(toDelete)){
            this.objCounter--;
            float loadFactor = (float)(this.size())/(this.capacity());
            if (loadFactor < this.getLowerLoadFactor() && this.capacity()>1) {
                this.currentCapacity = this.capacity()/2;
                this.rehashTable();
            }
            return true;
        }
        return false;
    }
}
