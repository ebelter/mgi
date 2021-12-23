/* id name type */
INSERT INTO 'entity' VALUES(1, 'H_G002', 'sample');
INSERT INTO 'entity' VALUES(2, 'GRCh38', 'reference');
/* entity_id group name value */
INSERT INTO 'entity_feature' VALUES(1, 'qc', 'qc_pass', '1');
INSERT INTO 'entity_feature' VALUES(2, 'qc', 'coverage', '30X');
/* id entity_id group value checksum exists kind */
INSERT INTO 'entity_path' VALUES(1, 1, 'analysis1', '/mnt/data/samples/HG002.merged.bam', 'checksum', 'merged bam', True);
INSERT INTO 'entity_path' VALUES(2, 2, 'no alt', '/mnt/data/references/GRCh38.fasta', 'checksum', 'fasta', True);
