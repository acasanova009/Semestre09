#include <stdio.h>
#include <mpi.h>

int main(int argc, char** argv) {
    int id, num_procesos;
    int dato;
    int recolectados[4];   // para gather en root


    MPI_Init(&argc, &argv);                       // Inicia MPI
    MPI_Comm_rank(MPI_COMM_WORLD, &id);     // ID del proceso
    MPI_Comm_size(MPI_COMM_WORLD, &num_procesos); // Total de procesos

   

        // Asignar manualmente un valor a cada proceso (sin scatter)
    if (id == 0) dato = 15;
    else if (id == 1) dato = 31;
    else if (id == 2) dato = 27;
    else if (id == 3) dato = 49;

    // Cada proceso avisa qué dato recibió
    printf("Proceso %d recibió dato = %d\n", id, dato);


    // Recolectar resultados en el root
    MPI_Gather(&dato, 1, MPI_INT,
               recolectados, 1, MPI_INT,
               0, MPI_COMM_WORLD);

    // Solo el root imprime los resultados
    if (id == 0) {
        printf("\nRoot recibió todos los resultados:\n");
        for (int i = 0; i < num_procesos; i++) {
            printf("recolectados[%d] = %d\n", i, recolectados[i]);
        }
        printf("\n");
    }

    MPI_Finalize();  // Finaliza MPI
    return 0;
}
