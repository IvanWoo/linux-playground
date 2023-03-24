#include "thread.h"
#include "thread-sync.h"

#define T 4
#define N 10000000

sem_t done;
long sum = 0;

// void atomic_inc(long *ptr) {
//   asm volatile(
//     "lock incq %0"
//     : "+m"(*ptr) : : "memory"
//   );
// }
void atomic_inc(long *ptr) {
  // https://stackoverflow.com/a/72577865
  __atomic_add_fetch(&sum, 1, __ATOMIC_SEQ_CST);
} 

void Tsum() {
  for (int i = 0; i < N; i++) {
    atomic_inc(&sum);
  }
  V(&done);
}

void Tprint() {
  for (int i = 0; i < T; i++) {
    P(&done);
  }
  printf("sum = %ld\n", sum);
}

int main() {
  SEM_INIT(&done, 0);
  for (int i = 0; i < T; i++) {
    create(Tsum);
  }
  create(Tprint);
}