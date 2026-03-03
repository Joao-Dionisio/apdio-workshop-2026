$pdf_mode = 1;              # use pdflatex
$aux_dir  = 'aux';          # auxiliary files (.aux, .log, .toc, …) go here
$out_dir  = '.';             # compiled PDF stays in slides/
$pdflatex = 'pdflatex -interaction=nonstopmode %O %S';

END {
  use File::Path qw(remove_tree);
  remove_tree('aux') if -d 'aux';
}
