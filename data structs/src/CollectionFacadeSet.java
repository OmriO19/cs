import java.util.*;

/**
 * Wraps an underlying Collection and serves to both simplify its API and give it a common type with the
 * implemented SimpleHashSets
 */
public class CollectionFacadeSet implements SimpleSet {

    protected Collection<String> collection;

    /**
     * Creates a new facade wrapping the specified collection.
     * @param collection - The Collection to wrap.
     */
    public CollectionFacadeSet(Collection<String> collection){
        this.collection = collection;
    }
    @Override
    public boolean add(String newValue) {
        if (this.contains(newValue))
            return false;
        else
            return this.collection.add(newValue);
    }
    @Override
    public boolean contains(String searchVal) {
        return this.collection.contains(searchVal);
    }
    @Override
    public boolean delete(String toDelete) {
        return this.collection.remove(toDelete);
    }
    @Override
    public int size() {
        return collection.size();
    }
}
