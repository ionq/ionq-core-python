# IonQ Core Examples

This directory contains usage examples for the `ionq-core` API.

## Running the Examples

1. **Install dependencies**
   Ensure you have installed the `ionq-core` package. If running from the repository source:
   ```sh
   pip install -e .
   ```
   You will also need `scipy` for the classical optimization example:
   ```sh
   pip install scipy
   ```

2. **Set your API Key**
   The IonQ client requires an API key to communicate with the cloud endpoints. Export it in your shell:
   ```sh
   export IONQ_API_KEY="your_api_key_here"
   ```

3. **Run the script**
   ```sh
   python examples/quantum_function_qaoa.py
   ```

## Example Index

- **`quantum_function_qaoa.py`**: Demonstrates the Hosted Hybrid Service (Quantum Functions) by minimizing a Max Cut Hamiltonian energy via the free simulator. It uses a custom OpenQASM ansatz (1 layer QAOA) and a client-side `scipy.optimize` loop.
