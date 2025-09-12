#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
    int id, num_procesos;
    int dato;
    int datos[4] = {15, 31, 27, 49}; // arreglo inicial en root

    MPI_Init(&argc, &argv);                        // Inicia MPI
    MPI_Comm_rank(MPI_COMM_WORLD, &id);            // ID del proceso
    MPI_Comm_size(MPI_COMM_WORLD, &num_procesos);  // Total de procesos

    // Repartir valores del arreglo con scatter
    MPI_Scatter(datos, 1, MPI_INT, &dato, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Cada proceso avisa qué dato recibió
    printf("Proceso %d recibió dato = %d\n", id, dato);

     // Solo el root imprime los resultados
    if (id == 0) {
        printf("\nEn root: \n");
        for (int i = 0; i < num_procesos; i++) {
            printf("Datos originales[%d] = %d\n", i, datos[i]);
        }
        printf("\n");
    }


    MPI_Finalize();  // Finaliza MPI
    return 0;
}
