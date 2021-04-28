public class matriz {
    public static int matrix(int[][] mat) {
        int contador = 0;
        int i = 1;

        for (int j = 0; j < mat[0].length && i < mat[0].length; j++) {
            contador += mat[j].length - i;
            i++;
        }
        return contador;
    }

    public static void main(String[] args) {
        int[][] matriz = { { -1, -4, -6, 7 }, { -3, -4, 5, 5 }, { -2, 9, 4, 5 } };
        long startTime = System.nanoTime();

        System.out.print(matrix(matriz));
        long stopTime = System.nanoTime();
        System.out.println(stopTime - startTime);

    }

}