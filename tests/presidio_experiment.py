from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

text = """
Solaire of Astora can be contacted at solaire@example.com.
His phone number is +91 00000 00000 and his IP address is 192.168.1.10.
"""

results = analyzer.analyze(
    text=text,
    language="en",
)

for result in results:
    print(
        result.entity_type,
        repr(text[result.start:result.end]),
        result.score,
    )
