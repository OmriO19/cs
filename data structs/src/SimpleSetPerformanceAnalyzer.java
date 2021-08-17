import java.util.*;
public class SimpleSetPerformanceAnalyzer {

    final private static int SEVENTY  = 70000;
    final private static int SEVEN  = 7000;
    final private static int MILLION = 1000000;
    final private static String NEG_NUMBER = "-13170890158";
    final private static String NUMBER = "23";
    final private static String HI = "hi";
    final private static String FOUND = "found";
    final private static String NOT_FOUND = "not found";
    final private static String[] data1 = Ex4Utils.file2array("data1.txt");
    final private static String[] data2 = Ex4Utils.file2array("data2.txt");
    private static Boolean bool = Boolean.TRUE;

    /**
     * the menu of the analyzer
     */
    public static void main(String[] args){
        Scanner menu = new Scanner(System.in);
        System.out.println("Please enter the option number. Some options can take some time...");
        System.out.println("Choose data structure");
        System.out.println("1 - openHashSet");
        System.out.println("2 - closedHashSet");
        System.out.println("3 - treeSet");
        System.out.println("4 - linkedList");
        System.out.println("5 - hashSet");
        int dataStructure = menu.nextInt();
        System.out.println("Choose the file you want to add");
        System.out.println("1 - data1");
        System.out.println("2 - data2");
        int file = menu.nextInt();
        String[] data;
        if (file == 1)
            data=data1;
        else
            data=data2;
        SimpleSet set;
        if (dataStructure == 1) {
            set = new OpenHashSet();
        } else if (dataStructure == 2) {
            set = new ClosedHashSet();
        } else if (dataStructure == 3) {
            set = new CollectionFacadeSet(new TreeSet<String>());
        } else if (dataStructure == 4) {
            set = new CollectionFacadeSet(new LinkedList<String>());
        } else {
            set = new CollectionFacadeSet(new HashSet<String>());
        }
        System.out.println(addData(data, set) + " ms");
        System.out.println("Choose the string you want to search for");
        System.out.println("1 - "+HI);
        System.out.println("2 - "+NEG_NUMBER);
        System.out.println("3 - "+NUMBER);
        int string = menu.nextInt();
        String str;
        if(string==1)
            str = HI;
        else if(string==2)
            str = NEG_NUMBER;
        else if(string==3)
            str = NUMBER;
        else {
            str = null;
            System.exit(0);
        }
        if(dataStructure==4)
            listContains(str, set);
        else
            contains(str, set);
    }

    /**
     * @param nanoseconds the time it took in nanoseconds
     * @return the time it took in nanoseconds in milliseconds
     */
    private static long milliseconds(long nanoseconds){
        return (nanoseconds/MILLION);
    }

    /**
     * @param data the data to add to the set
     * @param set the set to test
     * @return the time in milliseconds to add the data to the set
     */
    private static long addData(String[] data, SimpleSet set){
        long timeBefore = System.nanoTime();
        for (String string: data)
           set.add(string);
        long difference = System.nanoTime() - timeBefore;
        return(milliseconds(difference));
    }

    /**
     * print if the set contains or not the string and the time that took to search it
     * @param string the string to check
     * @param set the set to check
     */
    private static void contains(String string, SimpleSet set){
        for (int i = 0; i < SEVENTY; i++) {
           bool = set.contains(string);
        }
        long timeBefore = System.nanoTime();
        for (int i = 0; i < SEVENTY; i++) {
            bool = set.contains(string);
        }
        long difference = System.nanoTime() - timeBefore;
        if(bool)
            System.out.println(FOUND);
        else
            System.out.println(NOT_FOUND);
        System.out.println(difference/SEVENTY + " ns");
    }

    /**
     * @param string the string to search
     * @param set a linked list set
     */
    private static void listContains(String string, SimpleSet set){
        long timeBefore = System.nanoTime();
        for (int i = 0; i < SEVEN; i++) {
            bool = set.contains(string);
        }
        long difference = System.nanoTime() - timeBefore;
        if(bool)
            System.out.println(FOUND);
        else
            System.out.println(NOT_FOUND);
        System.out.println(difference/SEVEN + " ns");
    }
}
