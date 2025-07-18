from bitnet_api import BitNetClient

def test_cpu_non_streaming():
    print("=== CPU Non-Streaming ===")
    client = BitNetClient(device="cpu", verbose=True)
    response = client.send("Hello, CPU non-streaming!")
    print("Response:", response)

def test_cpu_streaming():
    print("\n=== CPU Streaming ===")
    client = BitNetClient(device="cpu", verbose=True)
    print("Response:", end=" ")
    for token in client.send("Hello, CPU streaming!", stream=True):
        print(token, end="", flush=True)
    print()

def test_gpu():
    print("\n=== GPU ===")
    client = BitNetClient(device="gpu", verbose=True)
    response = client.send("Hello, GPU!")
    print("Response:", response)

if __name__ == "__main__":
    test_cpu_non_streaming()
    test_cpu_streaming()
    test_gpu()
