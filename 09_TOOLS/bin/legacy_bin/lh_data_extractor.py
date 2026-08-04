#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
LongHun Data Extractor - From CSDN & Chat Logs
DNA: #龍芯⚡️2026-07-18-DATA-EXTRACT-v1.0
"""

import os
import json
import re
import argparse
from datetime import datetime

class CSDNExtractor:
    """Extract training data from CSDN blog posts"""

    def __init__(self, user_id):
        self.user_id = user_id
        self.dna = "#龍芯⚡️2026-07-18-CSDN-EXTRACT-v1.0"

    def extract(self, input_dir, output_file):
        """Extract from CSDN markdown files"""
        print(f"[EXTRACT] CSDN user: {self.user_id}")

        samples = []

        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract Q&A pairs from markdown
                    qa_pairs = self._parse_markdown(content)
                    samples.extend(qa_pairs)

        # Save
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')

        print(f"[DONE] Extracted {len(samples)} samples -> {output_file}")
        return samples

    def _parse_markdown(self, content):
        """Parse markdown into instruction-output pairs"""
        samples = []

        # Split by headers
        sections = re.split(r'#{2,4}\s+', content)

        for section in sections:
            if len(section) < 100:
                continue

            # Create instruction from first line
            lines = section.strip().split('\n')
            if not lines:
                continue

            instruction = lines[0][:100]
            output = '\n'.join(lines[1:])[:2000]

            samples.append({
                "instruction": instruction,
                "input": "",
                "output": output,
                "source": "csdn",
                "dna": self.dna
            })

        return samples

class ChatExtractor:
    """Extract from conversation logs"""

    def __init__(self):
        self.dna = "#龍芯⚡️2026-07-18-CHAT-EXTRACT-v1.0"

    def extract(self, input_dir, output_file):
        """Extract from chat log files"""
        print(f"[EXTRACT] Chat logs from: {input_dir}")

        samples = []

        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.json') or file.endswith('.txt'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    pairs = self._parse_chat(content)
                    samples.extend(pairs)

        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')

        print(f"[DONE] Extracted {len(samples)} samples -> {output_file}")
        return samples

    def _parse_chat(self, content):
        """Parse chat into instruction-output"""
        samples = []

        lines = content.split('\n')

        i = 0
        while i < len(lines) - 1:
            user_msg = lines[i].strip()
            if user_msg.startswith('User:') or user_msg.startswith('用户:'):
                instruction = user_msg.split(':', 1)[1].strip()

                if i + 1 < len(lines):
                    assistant_msg = lines[i + 1].strip()
                    if assistant_msg.startswith('Assistant:') or assistant_msg.startswith('AI:'):
                        output = assistant_msg.split(':', 1)[1].strip()

                        samples.append({
                            "instruction": instruction,
                            "input": "",
                            "output": output,
                            "source": "chat",
                            "dna": self.dna
                        })
                        i += 2
                        continue
            i += 1

        return samples

class DataMerger:
    """Merge and dedup multiple data sources"""

    def __init__(self, target_count=998):
        self.target_count = target_count
        self.dna = "#龍芯⚡️2026-07-18-DATA-MERGE-v1.0"

    def merge(self, input_files, output_file):
        """Merge multiple jsonl files, dedup, ensure 998 samples"""
        print(f"[MERGE] Target: {self.target_count} samples")

        all_samples = []
        seen_hashes = set()

        for filepath in input_files:
            if not os.path.exists(filepath):
                print(f"[SKIP] Not found: {filepath}")
                continue

            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        sample = json.loads(line)
                    except:
                        continue

                    # Dedup by content hash
                    content = sample.get('instruction', '') + sample.get('output', '')
                    h = hash(content[:200])

                    if h not in seen_hashes:
                        seen_hashes.add(h)
                        all_samples.append(sample)

        # Ensure minimum count
        if len(all_samples) < self.target_count:
            print(f"[WARN] Only {len(all_samples)} samples, need {self.target_count}")

        # Take top N
        final_samples = all_samples[:self.target_count]

        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            for sample in final_samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')

        print(f"[DONE] Merged {len(final_samples)} samples -> {output_file}")
        return final_samples

def main():
    parser = argparse.ArgumentParser(description='LongHun Data Extractor')
    parser.add_argument('--csdn_dir', default=os.path.expanduser('~/longhun-data/csdn/'))
    parser.add_argument('--chat_dir', default=os.path.expanduser('~/longhun-data/chats/'))
    parser.add_argument('--output', default=os.path.expanduser('~/longhun-data/clean_998.jsonl'))
    parser.add_argument('--target', type=int, default=998)
    args = parser.parse_args()

    # Extract CSDN
    csdn_out = os.path.expanduser('~/longhun-data/raw_csdn.jsonl')
    csdn = CSDNExtractor('UID9622')
    csdn.extract(os.path.expanduser(args.csdn_dir), csdn_out)

    # Extract Chat
    chat_out = os.path.expanduser('~/longhun-data/raw_chat.jsonl')
    chat = ChatExtractor()
    chat.extract(os.path.expanduser(args.chat_dir), chat_out)

    # Merge
    merger = DataMerger(args.target)
    merger.merge([csdn_out, chat_out], os.path.expanduser(args.output))

if __name__ == "__main__":
    main()
