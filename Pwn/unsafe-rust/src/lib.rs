//! So far, all our bugs are implemented using a single soundness hole in the Rust compiler.
//!
//! The explanation is detailed in the [`lifetime_expansion`] module.

#![deny(unsafe_code)]

// The actual exploit
pub mod lifetime_expansion;

// The bugs we created with the exploit
pub mod buffer_overflow;
pub mod transmute;

pub use lifetime_expansion::*;

pub use buffer_overflow::buffer_overflow;
pub use transmute::transmute;

/// Construct a [`String`] from a pointer, capacity and length, in a completely safe manner.
///
/// [`String`] is a `Vec<u8>` which is a `(RawVec, usize)` which is a `((Unique, usize), usize)`.
///
/// Rust explicitly says that structs are not guaranteed to have members in order,
/// so instead we determine that order at runtime.
///
/// # Safety
///
/// This function is 100% memory-safe.
///
/// Nevertheless, remember to use [`std::mem::forget`] to deallocate the fake [`String`], otherwise Rust
/// will think the pointer has been allocated by the global allocator and free it the wrong way.
///
/// > As they say: *Trust, but Verify.*
#[inline(always)]
pub fn construct_fake_string(ptr: *mut u8, cap: usize, len: usize) -> String {
  let sentinel_string = crate::transmute::<_, String>([0usize, 1usize, 2usize]);

  let mut actual_buf = [0usize; 3];
  actual_buf[sentinel_string.as_ptr() as usize] = ptr as usize;
  actual_buf[sentinel_string.capacity()] = cap;
  actual_buf[sentinel_string.len()] = len;

  std::mem::forget(sentinel_string);

  crate::transmute::<_, String>(actual_buf)
}