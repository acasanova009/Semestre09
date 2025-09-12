#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    int rank, size;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int n = 12; // tamaño de los arreglos
    int *A = NULL, *B = NULL;

    // El proceso 0 inicializa los arreglos
    if (rank == 0) {
        A = (int*)malloc(n * sizeof(int));
        B = (int*)malloc(n * sizeof(int));
        for (int i = 0; i < n; i++) {
            A[i] = i + 1;      // ejemplo: 1,2,3,...
            B[i] = (i + 1) * 2; // ejemplo: 2,4,6,...
        }
    }

    // Calcular cuántos elementos va a recibir cada proceso
    int elems_per_proc = n / size;
    int remainder = n % size; // si n no es divisible entre size

    int start_idx, end_idx;
    if (rank < remainder) {
        start_idx = rank * (elems_per_proc + 1);
        end_idx = start_idx + elems_per_proc;
    } else {
        start_idx = rank * elems_per_proc + remainder;
        end_idx = start_idx + elems_per_proc - 1;
    }
    int local_n = end_idx - start_idx + 1;

    // Cada proceso crea sus subarreglos locales
    int *local_A = (int*)malloc(local_n * sizeof(int));
    int *local_B = (int*)malloc(local_n * sizeof(int));

    // El proceso 0 envía los subarreglos a los demás procesos
    if (rank == 0) {
        for (int i = 1; i < size; i++) {
            int s_idx, e_idx, count;
            if (i < remainder) {
                s_idx = i * (elems_per_proc + 1);
                e_idx = s_idx + elems_per_proc;
            } else {
                s_idx = i * elems_per_proc + remainder;
                e_idx = s_idx + elems_per_proc - 1;
            }
            count = e_idx - s_idx + 1;
            MPI_Send(&A[s_idx], count, MPI_INT, i, 0, MPI_COMM_WORLD);
            MPI_Send(&B[s_idx], count, MPI_INT, i, 1, MPI_COMM_WORLD);
        }
        // proceso 0 copia sus elementos locales
        for (int i = 0; i < local_n; i++) {
            local_A[i] = A[i];
            local_B[i] = B[i];
        }
    } else {
        MPI_Recv(local_A, local_n, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
        MPI_Recv(local_B, local_n, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
    }

    // Calcular el producto punto parcial
    int local_dot = 0;
    for (int i = 0; i < local_n; i++) {
        local_dot += local_A[i] * local_B[i];
    }

    printf("Proceso %d calcula producto punto parcial = %d\n", rank, local_dot);

    // Enviar resultados al proceso 0
    if (rank != 0) {
        MPI_Send(&local_dot, 1, MPI_INT, 0, 2, MPI_COMM_WORLD);
    } else {
        int total_dot = local_dot;
        int recv_dot;
        for (int i = 1; i < size; i++) {
            MPI_Recv(&recv_dot, 1, MPI_INT, i, 2, MPI_COMM_WORLD, &status);
            total_dot += recv_dot;
        }
        printf("Producto punto total = %d\n", total_dot);
    }

    free(local_A);
    free(local_B);
    if (rank == 0) {
        free(A);
        free(B);
    }

    MPI_Finalize();
    return 0;
}