/**
 * A tuple of a string object and his hashcode
 */
public class Tuple{
    /**
     * the string that the object holds
     */
    public final String string;
    /**
     * represent the status of the string in the table, exist or have been deleted
     */
    private boolean status;

    /**
     * represent the object as deleted
     */
    private final boolean DELETED = false;

    /**
     * constructor for the tuple
     * @param string the string object
     */
    public Tuple(String string){
        this.string = string;
        this.status = true;
    }

    @Override
    public boolean equals(Object obj) {
        return this.string.equals(obj);
    }

    /**
     * @return true if the object deleted, false otherwise
     */
    public boolean isDeleted(){
        return (this.status == DELETED);
    }

    /**
     * mark the object as deleted
     */
    public void Delete(){
        this.status = DELETED;
    }
}
