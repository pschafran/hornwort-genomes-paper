#! /usr/bin/env Rscript
d<-scan("stdin", quiet=TRUE)
cat(print("Sum:"), sum(d), print("Min:"),min(d),print("Max:"), max(d), print("Median:"), median(d),print("Mean:"), mean(d),print("Std. Dev:"), sd(d),   sep="\n")
