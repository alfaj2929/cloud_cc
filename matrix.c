#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

#define SIZE 1000

int main(int argc, char *argv[]) {
    int rank, size;
    int i, j, k;
    double a[SIZE][SIZE], b[SIZE][SIZE], c[SIZE][SIZE];
    double start_time, end_time;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Initialize matrices on master
    if (rank == 0) {
        for (i = 0; i < SIZE; i++) {
            for (j = 0; j < SIZE; j++) {
                a[i][j] = (double)(i + j);
                b[i][j] = (double)(i - j);
                c[i][j] = 0.0;
            }
        }
        start_time = MPI_Wtime();
    }

    // Broadcast matrices a and b to all processes
    MPI_Bcast(a, SIZE * SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    MPI_Bcast(b, SIZE * SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Compute partial matrix multiplication
    int rows_per_process = SIZE / size;
    int start_row = rank * rows_per_process;
    int end_row = start_row + rows_per_process;

    for (i = start_row; i < end_row; i++) {
        for (j = 0; j < SIZE; j++) {
            for (k = 0; k < SIZE; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }

    // Gather results to master
    MPI_Gather(c[start_row], rows_per_process * SIZE, MPI_DOUBLE,
               c, rows_per_process * SIZE, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Master prints execution time
    if (rank == 0) {
        end_time = MPI_Wtime();
        printf("Matrix multiplication completed in %f seconds\n", end_time - start_time);
    }

    MPI_Finalize();
    return 0;
}
