import java.util.*;
/**
 * A LinkedList that extends the CollectionFacadeSet
 */
public class ListLinked extends CollectionFacadeSet{

    /**
     * The constructor of the class gives CollectionFacadeSet a LinkedList<String> object
     */
    public ListLinked(){
        super(new LinkedList<String>());
    }

    /**
     * @return iterator - the collection iterator
     */
    public Iterator<String> iterator(){
        return this.collection.iterator();
    }
}
