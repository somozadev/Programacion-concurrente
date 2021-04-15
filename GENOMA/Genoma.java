public class Genoma {

    public static int GenomaCalculator(int start, int end) {
        int cuantity = end - start;
        if (cuantity > 0)
            return GenomaDnW(start, end);
        else
            return -1;
    }

    public static int GenomaDnW(int start, int end) {
        int returner = 0;
        int halfEnd = (end - start) / 2;
        System.out.println("Halfend : " + halfEnd);

        if (halfEnd  > 100)  // 20.000.000 as base case
        {
            start = GenomaDnW(start, halfEnd);
            halfEnd = GenomaDnW(halfEnd, end);
            System.out.println("start : " + start);
            System.out.println("halfEnd : " + halfEnd);
        } 
        else 
        {

        }
        
        

        return returner;
    }

    public static void main(String[] args) {
        System.out.println(GenomaCalculator(124000, 294000));
    }
}