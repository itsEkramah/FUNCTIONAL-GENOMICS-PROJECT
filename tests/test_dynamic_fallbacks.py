import os
import unittest
import tempfile
from backend.services.diamond_service import run_diamond_blastp
from backend.services.hmmer_service import run_hmmer_hmmscan

class MockLogger:
    def info(self, msg): pass
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

class TestDynamicFallbacks(unittest.TestCase):
    def setUp(self):
        self.logger = MockLogger()
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        self.temp_dir.cleanup()

    def test_dynamic_diamond_homology(self):
        # Create a temp FASTA with one sequence close to Spike protein (perfect match)
        spike_like_fasta = os.path.join(self.temp_dir.name, "spike_like.fasta")
        with open(spike_like_fasta, "w", encoding="utf-8") as f:
            f.write(">seq_1\n")
            # Close sequence to Spike glycoprotein (P0DTC2_SPIKE sample sequence)
            f.write("MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFYSNVTWFHAIHVSGTNGTKRFDNPVLPF\n")

        # Create a temp FASTA with one sequence close to Capsid protein (with mutations / mismatches)
        capsid_like_fasta = os.path.join(self.temp_dir.name, "capsid_like.fasta")
        with open(capsid_like_fasta, "w", encoding="utf-8") as f:
            f.write(">seq_1\n")
            # Mutate characters to 'X' to introduce mismatches relative to capsid reference
            f.write("MDIDPYKEFGATVELLSFLPSXXXXXSRDLLDTASALYREALESPXXXXXHHTALRQAILCWGELMXXXXW\n")

        # Run DIAMOND fallback for Spike-like sequence
        out_spike_tsv = os.path.join(self.temp_dir.name, "spike_hits.tsv")
        spike_hits = run_diamond_blastp(spike_like_fasta, "dummy_db", out_spike_tsv, self.logger)
        
        # Run DIAMOND fallback for Capsid-like sequence
        out_capsid_tsv = os.path.join(self.temp_dir.name, "capsid_hits.tsv")
        capsid_hits = run_diamond_blastp(capsid_like_fasta, "dummy_db", out_capsid_tsv, self.logger)

        self.assertEqual(len(spike_hits), 1)
        self.assertEqual(len(capsid_hits), 1)
        
        # Verify that hit subjects differ based on sequence similarity
        self.assertEqual(spike_hits[0]["subject_protein"], "P0DTC2_SPIKE")
        self.assertEqual(capsid_hits[0]["subject_protein"], "P03135_CAPSID")
        
        # Assert that changing query sequence changes pident and evalue
        self.assertNotEqual(spike_hits[0]["identity_percent"], capsid_hits[0]["identity_percent"])
        self.assertNotEqual(spike_hits[0]["evalue"], capsid_hits[0]["evalue"])

    def test_dynamic_pfam_domains(self):
        # Create a temp FASTA with one sequence close to Spike protein (perfect match)
        spike_like_fasta = os.path.join(self.temp_dir.name, "spike_like.fasta")
        with open(spike_like_fasta, "w", encoding="utf-8") as f:
            f.write(">seq_1\n")
            f.write("MFVFLVLLPLVSSQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFYSNVTWFHAIHVSGTNGTKRFDNPVLPF\n")

        # Create a temp FASTA with one sequence close to Nucleoprotein (with mutations / mismatches)
        nucleo_like_fasta = os.path.join(self.temp_dir.name, "nucleo_like.fasta")
        with open(nucleo_like_fasta, "w", encoding="utf-8") as f:
            f.write(">seq_1\n")
            f.write("MSDNGPQNQRNAPRITFGGPSDSTGSNQNGXXXXXXARSKQRRPQGLPNNTASWFTALTQHGKEDLKFPRGQGVPXXXXXSSPDDQIGY\n")

        # Run Pfam fallback for Spike-like sequence
        spike_domains = run_hmmer_hmmscan(spike_like_fasta, "dummy_db", os.path.join(self.temp_dir.name, "spike_dom"), self.logger)
        
        # Run Pfam fallback for Nucleo-like sequence
        nucleo_domains = run_hmmer_hmmscan(nucleo_like_fasta, "dummy_db", os.path.join(self.temp_dir.name, "nucleo_dom"), self.logger)

        self.assertEqual(len(spike_domains), 1)
        self.assertEqual(len(nucleo_domains), 1)
        
        # Verify that domain predictions differ based on sequence similarity
        self.assertEqual(spike_domains[0]["pfam_name"], "Corona_S2")
        self.assertEqual(nucleo_domains[0]["pfam_name"], "Paramyxo_NC")
        
        # Assert that coordinates and evalues are dynamic
        self.assertNotEqual(spike_domains[0]["evalue"], nucleo_domains[0]["evalue"])

if __name__ == "__main__":
    unittest.main()
