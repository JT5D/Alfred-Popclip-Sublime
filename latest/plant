#!/usr/bin/ruby
PLANTER_VERSION = "2.1.4"
=begin
Planter v2.0.0
Brett Terpstra 2013
Ruby script to create a directory structure from indented data.

Three ways to use it:
- Pipe indented (tabs or 2 spaces) text to the script
  - e.g. `cat "mytemplate" | plant
- Create template.tpl files in ~/.planter and call them by their base name
  - e.g. Create a text file in ~/.planter/site.tpl
  - `plant site`
- Call plant without input and it will open your $EDITOR to create the
tree on the fly

You can put %%X%% variables into templates (.tpl files stored in
`~/.planter/`), where X is a number that corresponds to the index of the
argument passed when planter is called. e.g. `plant client "Mr. Butterfinger"`
would replace %%1%% in client.tpl with "Mr. Butterfinger". Use %%X|default%%
to make a variable optional with default replacement. Variables can be
repeated to reuse an argument, and each repeated identifier can have different
defaults.

If you want to specify variables for just some positions, use "-" or "." for
arguments in the command to force the default for that position.

If a line in the template matches a file or folder that exists in ~/.planter,
that file/folder will be copied to the destination folder. **Make sure that the
last line before a nested section is the name of the parent folder.**

Set tags on created folder and copied items items by adding @TAGs at the end
of the line in the template. To make a variable placeholder function as a tag,
put the @ between the % and the replacement number at the beginning (e.g.
`%%@2%%` or `%%@1|default%%`). Unless the --no-tagify option is used,
variables identified as tags will have spaces removed and be lowercased. Tags
set on a folder or file will replace existing tags.

The @ symbol is removed by default. To add a character prefix to ALL tags, use
"--tag-prefix @" on the command line. Otherwise, just include any symbols or
characters needed on a one-off basis in the arguments passed to a template, or
include them in the template.

  // test.tpl
  // tag "folder name" with "foldertag" and "@foldertype"
  folder name @foldertag @@foldertype


Add comments in templates with "//". This can be anywhere in a line, anything
after it will be ingored.

Entirely optionally, the template can end with a ruby script. Separate the
script from the template with "---". It will be executed after the folders are
created, and any variable placeholders in it will be replaced with command
line arguments, just like in the template. You can use this to perform
additional operations, notifications or further customize Planter's
functionality. To execute scripts in other languages, use Ruby's system call:

  system "python /path/to/script.py"

  # or

  %x{python "path/to/script.py"}

No hashbang is necessary in the script.

For a list of command line options, use `plant -h`.
=end
require 'yaml'
require 'tmpdir'
require 'fileutils'
require 'optparse'
require 'shellwords'

def show_version
  $stdout.puts "Planter v#{PLANTER_VERSION}"
end

def show_help
  help =<<EOHELP
Pass a template on STDIN, by name from ~/.planter/
or run `plant` by itself to edit a temporary template
in $EDITOR. Pass addition variable replacements to
templates as ordered arguments.

Examples:

plant

cat outline.txt | plant

plant project "Client Name" design
EOHELP
  $stdout.puts help
end

options = {}
optparse = OptionParser.new do|opts|
  opts.banner = "Create a folder hierarchy from tab-intended lists."
  opts.on( '-h', '--help', 'Display this screen' ) do
    show_version
    puts opts
    show_help
    Process.exit
  end

  opts.on('-v', '--version', 'Display version and exit') do
    show_version
    Process.exit
  end

  options[:color] = true
  $color_output = true
  opts.on( '--no-color', 'Turn off color terminal output' ) do
    $color_output = false
    options[:color] = false
  end

  options[:tag_prefix] = ""
  opts.on( '-p PREFIX', '--tag-prefix PREFIX', 'Message to send' ) do |prefix|
    options[:tag_prefix] = prefix
  end

  options[:tagify] = true
  opts.on( '--no-tagify', 'Do not lowercase and remove whitespace on variables set as tags' ) do
    options[:tagify] = false
  end
end

optparse.parse!


def color(color,dark=nil)
  return "" unless $color_output
  pre = dark.nil? || !dark ? "1;" : "0;"
  case color
  when "black"
    "\033[#{pre}30m"
  when "red"
    "\033[#{pre}31m"
  when "green"
    "\033[#{pre}32m"
  when "yellow"
    "\033[#{pre}33m"
  when "blue"
    "\033[#{pre}34m"
  when "magenta"
  when "purple"
    "\033[#{pre}35m"
  when "cyan"
    "\033[#{pre}36m"
  when "white"
    "\033[#{pre}37m"
  else
    "\033[0;39m"
  end
end

def get_hierarchy(input,parent=".",dirs_to_create=[])
  unless input && input.length > 0
    $stderr.puts "#{color("yellow")}get_hierarchy: #{color("red")}Input received is nil#{color("default")}"
    Process.exit
  end
  input.each do |dirs|
    if dirs.kind_of? Hash
      dirs.each do |k,v|
        tags = k.to_s.scan(/(?mi)@(\S[^@ ]+)/).map {|a| a[0].strip }
        dir = k.to_s.gsub(/(?mi)@(\S*[^@ ]*|$)/,'').strip
        dirs_to_create.push([File.expand_path("#{parent}/#{dir}"),tags])
        dirs_to_create = get_hierarchy(v,"#{parent}/#{dir}",dirs_to_create)
      end
    elsif dirs.kind_of? Array
      dirs_to_create = get_hierarchy(dirs,parent,dirs_to_create)
    elsif dirs.kind_of? String
      tags = dirs.scan(/(?mi) @(\S[^@ ]+)/).map {|a| a[0].strip }
      dir = dirs.gsub(/(?mi) @(\S*[^@ ]*|$)/,'').strip
      dirs_to_create.push([File.expand_path("#{parent}/#{dir.strip}"),tags])
    end
  end
  dirs_to_create
end

def text_to_yaml(input, options, replacements=[])

  if input.nil?
    $stderr.puts "#{color("yellow")}text_to_yaml: #{color("red")}Input received is nil#{color("default")}"
    Process.exit
  end
  # remove "//" comments
  input = input.gsub(/(\s|^)\/\/(.*|$)/,"").gsub(/^\s*\n/,'')

  # separate script
  split_input = input.split(/^[\-~]{3}\s*$/)
  input = split_input[0]

  script = split_input.length == 2 ? split_input[1] : ""

  variables_count = 0
  variables_count = input.scan(/%%@?(\d+)%%/).map {|match| match[0].to_i }.uniq.length
  if variables_count > replacements.length
    $stderr.puts("#{color("red")}Mismatched variable/replacement count#{color("default")}")
    $stderr.puts("Template has #{variables_count.to_s} required replacements, #{replacements.length.to_s} provided.")
    $stderr.puts
    $stderr.puts("#{color("yellow")}Template:\n=========#{color("white")}")
    $stderr.puts(input.split(/^[~\-]{3}$/)[0].gsub(/%%@*(\d)(\|[^%]*)?%%/,%Q{%%#{color("red",true)}\\1#{color("white")}%%}))
    $stderr.puts(color("default"))
    Process.exit 1
  end

  [script,input].map! do |string|
    string.gsub!(/%%(@+)?(\d+)(?:(\|)(.*?)?)?%%/m) do
      tag = $1.nil? ? "" : $1
      id = $2.to_i - 1
      has_default = $3
      default = $4

      if replacements[id] =~ /^[\-\.]$/
        if has_default == ""
          print "Argument specified to use default, but default not provided in template."
          Process.exit 1
        else
          default == "" ? "" : tag + default
        end

      else
        if replacements[id]
          rep = tag + replacements[id]
        elsif default !~ /^\s*$/
          rep = tag + default
        elsif default == ""
          rep = ""
        else
          print "Invalid or missing variable for placeholder #{id}"
          Process.exit 1
        end

        if tag.length > 0 && options[:tagify]
          rep.gsub(/\s*/,'').downcase
        else
          rep
        end

      end
    end
  end

  if input =~ /\//
    $stderr.puts "#{color("red")}  Error: #{color("white")}Input contains a \"/\" (not allowed)#{color("default")}"
    Process.exit
  end

  lines = input.split(/[\n\r]/)

  prev_indent = 0
  lines.each_with_index do |line, i|
    indent = line.gsub(/  /,"\t").match(/(\t*).*$/)[1]
    if indent.length > prev_indent
      lines[i-1] = lines[i-1].chomp + ":"
    end
    prev_indent = indent.length
    lines[i] = indent.gsub(/\t/,'  ') + "- " + lines[i].strip # unless indent.length == 0
  end
  lines.delete_if {|line|
    line == ''
  }

  ["---\n" + lines.join("\n"), script]
end

if STDIN.stat.size > 0
  data = STDIN.read
elsif ARGV.length > 0
  template = File.expand_path("~/.planter/#{ARGV[0].gsub(/\.tpl$/,'')}.tpl")
  ARGV.shift
  if File.exists? template
    File.open(template, 'r') do |infile|
      data = infile.read
    end
  else
    $stderr.puts "#{color("red")}Specified template not found in ~/.planter/*.tpl#{color("default")}"
    Process.exit
  end
else
  tmpfile = File.expand_path(Dir.tmpdir + "/planter.tmp")
  f = File.new(tmpfile, 'a+')
  f.puts "// Enter a tab indented folder hierarchy to create\n"
  f.close
  at_exit {FileUtils.rm(tmpfile) if File.exists?(tmpfile)}

  %x{$EDITOR "#{tmpfile}"}
  data = ""
  File.open(tmpfile, 'r') do |infile|
    data = infile.read
  end
end

if data.gsub(/\/\/.*/,'').gsub(/^\s*$/,'').length == 0
  $stderr.puts "#{color("red")}Empty input#{color("default")}"
  Process.exit
end

data.strip!
begin
  text, script = text_to_yaml(data,options,ARGV)
  yaml = YAML.load(text)
  unless yaml
    $stderr.puts "#{color("yellow")}YAML: #{color("red")}Failed processing text as YAML#{color("default")}"
    Process.exit
  end
rescue Exception => e
  # p e
  $stderr.puts("#{color("red",true)}Error in input#{color("default")}")
  Process.exit
end

dirs_to_create = get_hierarchy(yaml)

curr_dir = ENV['PWD']
root = File.join(curr_dir, dirs_to_create[0][0])

dirs_to_create.each do |dir|
  tags = dir[1]
  dir = dir[0]

  existed = false
  # dir.gsub!(/@\S+/,"").strip!
  unless File.exists? dir
    tagstring = tags.length > 0 ? " #{color("white",true)}[#{color("yellow",true)}#{tags.join(', ')}#{color("white",true)}]#{color("default")}" : ""

    if File.exists?(File.join(File.expand_path("~/.planter"),File.basename(dir)))
      $stderr.puts "#{color("yellow")}  Copy: #{color("white")}#{dir.sub(/^#{curr_dir}\//,'')}#{tagstring}#{color("default")}"
      FileUtils.cp_r(File.join(File.expand_path("~/.planter"),File.basename(dir)), dir)
    else
      $stderr.puts "#{color("yellow")}Create: #{color("white")}#{dir.sub(/^#{curr_dir}\//,'')}#{tagstring}#{color("default")}"
      Dir.mkdir(dir)
    end
  else
    existed = true
    $stderr.puts "#{color("yellow")}Exists: #{color("white")}#{dir.sub(/^#{curr_dir}\//,'')} #{color("red")}(file exists)#{color("default")}"
  end

  if tags.length > 0

    tags.map! {|tag| options[:tag_prefix] + tag } if options[:tag_prefix].length > 0
    if existed
      $stderr.puts "   #{color("yellow")}Tag: #{color("white")}#{dir.sub(/^#{curr_dir}\//,'')} #{color("white",true)}[#{color("yellow",true)}#{tags.join(', ')}#{color("white",true)}]#{color("default")}"
    end

    tags.map! {|tag|
      "<string>#{tag}</string>"
    }
    %x{xattr -w com.apple.metadata:_kMDItemUserTags '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array>#{tags.join()}</array></plist>' "#{dir}"}
    # %x{/usr/local/bin/openmeta -a #{tags.join(" ")} -p "#{dir}"} if tags.length > 0
  end


end

if script && script.length > 0
  begin
    eval(script)
  rescue Exception => e
    p e
    puts "Error running script."
  end
end

$stderr.puts "\n#{color("yellow")}Finished#{color("default")}"
