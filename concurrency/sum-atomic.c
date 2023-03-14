#include "thread.h"

#define N 100000000

long sum = 0;

// x86 assembly
// void atomic_inc(long *ptr) {
//   asm volatile(
//     "lock incq %0"  // Atomic + memory fence
//     : "+m"(*ptr)
//     :
//     : "memory"
//   );
// }

void atomic_inc(long *ptr) {
  // https://stackoverflow.com/a/72577865
  __atomic_add_fetch(&sum, 1, __ATOMIC_SEQ_CST);
} 

void Tsum() {
  for (int i = 0; i < N; i++) {
    atomic_fetch_add(&sum, 1);
  }
}

int main() {
  create(Tsum);
  create(Tsum);
  join();
  printf("sum = %ld\n", sum);
}