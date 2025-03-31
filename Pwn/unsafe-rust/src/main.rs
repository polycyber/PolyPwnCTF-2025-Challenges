#![deny(unsafe_code)]

use std::io;

use clap::{
  builder::{styling::AnsiColor, Styles},
  crate_authors, crate_description, crate_name, crate_version, value_parser, Arg, ArgAction,
  Command,
};
use clap_complete::{generate, Generator, Shell};
fn build_cli() -> Command {
  Command::new(crate_name!())
    .arg_required_else_help(true)
    .author(crate_authors!())
    .about(crate_description!())
    .version(crate_version!())
    .long_about(HELP)
    .subcommand(
      Command::new("solve").about("Solve the puzzle that protects the Prieure de la Rouille's secret."),
    )
    .styles(STYLE)
    .help_template(TEMPLATE)
}
fn main() {
  let mut command = build_cli();
  let matches = build_cli().clone().get_matches();
  let subcommand = matches.subcommand().unwrap();
  match subcommand.0 {
    "solve" => cve_rs::buffer_overflow().unwrap(),
    "completions" => print_completions(
      subcommand.1.get_one::<Shell>("shell").copied().unwrap(),
      &mut command,
    ),
    _ => unreachable!(),
  }
}

fn print_completions<G: Generator>(gen: G, cmd: &mut Command) {
  generate(gen, cmd, cmd.get_name().to_string(), &mut io::stdout());
}

const STYLE: Styles = Styles::styled()
  .header(AnsiColor::Yellow.on_default())
  .usage(AnsiColor::Green.on_default())
  .literal(AnsiColor::Green.on_default())
  .placeholder(AnsiColor::Green.on_default());

const TEMPLATE: &str = "\
{before-help}{name} {version}
{author-with-newline}{about-with-newline}
{usage-heading} {usage}

{all-args}{after-help}
";

const HELP: &str = r"
This *might* be inspired by cve-rs.
";