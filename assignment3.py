#! /usr/bin/env python3

import json
import vcf
import httplib2

__author__ = 'Lukas HUBER'

##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
## 4) View the VCF in a browser
##

class Assignment3:
    
    def __init__(self, file):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = file
        print("vcf file =", file)

    def annotate_vcf_file(self):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''    
        print("Annotating vcf file")
        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'
        
        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')
        
        self.annotation_result_json = json.loads(annotation_result)
        return self.annotation_result_json
    
    
    def get_list_of_genes(self):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''
        print("List of genes:")
        for i in self.annotation_result_json:
            if 'cadd' in i:
                if 'genename' in i['cadd']['gene']:
                    print("     ", i['cadd']['gene']['genename'])
    
    
    def get_num_variants_modifier(self):
        '''
        Print the number of variants with putative_impact "MODIFIER"
        :return:
        '''
        num_variants_modifier = 0
        for i in self.annotation_result_json:
            if 'snpeff' in i:
                key, value = "putative_impact", "MODIFIER"
                if key in i['snpeff']['ann'] and value == i['snpeff']['ann']['putative_impact']:
                    num_variants_modifier += 1
        print("Number of variants modifier:                       ",num_variants_modifier)
        
    
    def get_num_variants_with_mutationtaster_annotation(self):
        '''
        Print the number of variants with a 'mutationtaster' annotation
        :return:
        '''
        variants_with_mutationtaster_annotation = 0
        for i in self.annotation_result_json:
            if 'dbnsfp' in i:
                if 'mutationtaster' in i['dbnsfp']:
                    variants_with_mutationtaster_annotation += 1
        print("Number of variants with mutationtaster annotation: ",variants_with_mutationtaster_annotation)
        
    
    def get_num_variants_non_synonymous(self):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''
        variants_non_synonymous = 0
        for i in self.annotation_result_json:
            if 'cadd' in i:
                key, value = "consequence", "NON_SYNONYMOUS"
                if key in i['cadd'] and value == i['cadd']['consequence']:
                    variants_non_synonymous += 1
        print("Number of variants non synonymous:                 ", variants_non_synonymous)
        
    
    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''
   
        ## Document the final URL here
        print("TODO")
            
    
    def print_summary(self):
        self.annotate_vcf_file()
        print("\n---------------------- RESULTS ----------------------")
        self.get_list_of_genes()
        self.get_num_variants_modifier()
        self.get_num_variants_with_mutationtaster_annotation()
        self.get_num_variants_non_synonymous()
        print("-----------------------------------------------------\n")
    
    
def main():
    file = "chr16.vcf"
    print("Assignment 3")
    assignment3 = Assignment3(file)
    assignment3.print_summary()
    print("Done with assignment 3")
        
        
if __name__ == '__main__':
    main()
   
    



