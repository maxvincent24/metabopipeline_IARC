print(search())
print(.libPaths())
.libPaths(c(.libPaths(), "/home/vincentm/R/x86_64-pc-linux-gnu-library/4.0", "/opt/R/4.0.4/lib/R/library"))
print(.libPaths())

#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

print(args[1])
print(args[2])
print(args[3])

list_methods <- eval(parse(text=args[3]))
print(list_methods)


# Package names
#packages <- c("mice", "sjmisc")

# Install packages not yet installed
#installed_packages <- packages %in% rownames(installed.packages())
#if (any(installed_packages == FALSE)) {
#  install.packages(packages[!installed_packages])
#}

# Packages loading
#invisible(lapply(packages, library, character.only = TRUE))



require(mice)
require(sjmisc)




peakTable <- read.csv(args[1], sep = ',')
X <- peakTable[, grepl('variable', names(peakTable))]

predictorMatrix <- quickpred(X, mincor = 0.5, minpuc = 0.1, method = "pearson")


impute_with_MICE <- function(X, list_methods){
    
    # Compute predictor matrix
    predictorMatrix <- quickpred(X, mincor = 0.5, minpuc = 0.1, method = "pearson")
    
    for (method in list_methods){
        
        message(paste(rep('-', 100), collapse=''))
        message(paste(c(rep('-', (100 - (nchar(method) + 2)) %/% 2), ' ', method, ' ', rep('-', (100 - (nchar(method) + 2) + 1) %/% 2)), collapse=''))
        message('...Computing...')
        message('...............')

        start_time <- Sys.time()

        invisible(capture.output(imp <- mice(X, method = method, m = 5, maxit = 5, predictorMatrix = predictorMatrix, seed=1234, remove.collinear=FALSE))) # Impute data
        X_imp_merged <- merge_imputations(X, imp) # return data frame with imputed variables
        
        X_imp_merged_full <- cbind(X_imp_merged, X[, names(colSums(is.na(X))[colSums(is.na(X)) == 0])])
        X_imp_merged_full <- X_imp_merged_full[,names(X)]
        
        filename <- paste(args[2], '/X_R_MICE_', gsub('\\.', '_', method), '.csv', sep='')
        write.csv(X_imp_merged_full, filename, row.names = FALSE)
        
        x <- Sys.time() - start_time
        print(x)
        #message(paste(sapply(strsplit(as.character(x), "\\."), "[", 1), 'min', floor(as.numeric(substring(sapply(strsplit(as.character(x), "\\."), "[", 2), 1, 2)) * 0.6), 'sec', sep=' '))
        #message(paste(format(x, "%T")))
        message(paste(rep('-', 100), collapse=''))
        message('\n\n')
        
    }
    
}


impute_with_MICE(X, list_methods)



