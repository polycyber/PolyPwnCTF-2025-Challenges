//! A memory-safe buffer overflow.
//!
//! We allocate a slice on the stack, then transmute it into a String with a large capacity.
//! Then, we read input from stdin into that String. This overwrites another stack-allocated
//! slice, and then we can check if it's successfully overwritten.

use std::io::{stdin, stdout, Write, BufReader, BufRead};
//use std::time::Duration;
use std::{io, mem, str};
use std::fs::File;

use crate::construct_fake_string;

fn slice_to_num(buff: &[u8]) -> u32 {
    let bytes_buffer = buff.try_into();
  match bytes_buffer {
    Ok(bytes) => return u32::from_ne_bytes(bytes),
    _ => panic!()
  }
}

/// Perform a buffer overflow.
///
/// This is implemented in the form of a little password cracking game in the terminal.
#[inline(never)]
pub fn buffer_overflow() -> io::Result<()> {
  use std::hint::black_box;

  #[repr(C)]
  #[derive(Copy, Clone, Default)]
  struct Message {
    content: [u8; 32],
    message_index: [u8; 4],
  }

  let flag_file = File::open("flag.txt").unwrap();

  let mut flag_file_reader: BufReader<std::fs::File> = BufReader::new(flag_file);

  let mut flag_content: String = String::from("");

  flag_file_reader.read_line(&mut flag_content).unwrap();

  let flag_message_num = slice_to_num(&[1, 3, 3, 7]);

  let mut flag_message = black_box(Message::default());

  let flag_len = flag_content.len();

  let flag_chars = flag_content.into_bytes();


  for i in 0..flag_len {
    flag_message.content[i] = flag_chars[i];
  }

  flag_message.message_index = [1, 3, 3, 7];

  let mut message_vec : Vec<Message> = Vec::new();

  message_vec.push(flag_message);

  println!("Flag is at: {}", flag_message_num);

  let mut message = black_box(Message::default());

  // No one will ever have the time to type more than 1024 characters... ;v
  let mut content = construct_fake_string(message.content.as_mut_ptr(), 2048, 0usize);

  message.message_index = [0, 0, 0, 0];

  print!("Insert a new book in the library. Provide the title of the book: ");
  stdout().flush()?;
  stdin().read_line(&mut content)?;

  // If we don't forget our fake String, Rust will try to deallocate it as if it was a heap pointer.
  mem::forget(content);
  let message_num = slice_to_num(&message.message_index);

  println!("\nYour message is at: {}", message_num);

  message_vec.push(message);

  for tmp_message in message_vec {
    let tmp_message_num = slice_to_num(&tmp_message.message_index);
    if message_num == tmp_message_num {
      println!("FLAG: {:?}", tmp_message.content);
    }
  }

  Ok(())
}
