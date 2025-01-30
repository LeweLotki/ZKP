# Zero-Knowledge Proof Application (Schnorr Protocol)

This repository implements a Zero-Knowledge Proof (ZKP) system based on the Schnorr protocol. The project allows a client to prove to a server that they possess a secret (in this case, the checksum of a file) without ever revealing the secret itself. It demonstrates a secure way to validate file integrity and ownership through cryptographic methods while maintaining privacy.

---

## Table of Contents
1. [How to Run the Application](#how-to-run-the-application)
2. [How the Schnorr Protocol Works](#how-the-schnorr-protocol-works)
3. [Explanation of the Code](#explanation-of-the-code)
4. [System Architecture and Workflow](#system-architecture-and-workflow)
5. [Future Improvements](#future-improvements)

---

## How to Run the Application

The application is containerized using Docker, making it easy to set up and run. Follow the instructions below to deploy and interact with the system:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LeweLotki/ZKP.git
   cd ZKP 
   ```

2. **Build and Start the Containers**:
   Use Docker Compose to build the images and start the containers in detached mode:
   ```bash
   docker compose up -d --build
   ```

3. **Verify Running Containers**:
   Check that the server and database are running:
   ```bash
   docker ps
   ```

4. **Run the Client**:
   By default, the client container starts in a sleep mode to allow manual execution. Run the client logic using the following command:
   ```bash
   docker exec -it zkp-client-1 python -m app.main
   ```

5. **Stop and Clean Up**:
   To stop all containers and remove associated volumes, use:
   ```bash
   docker compose down -v
   ```

This setup ensures the system is easy to deploy and operate while maintaining clear separation between the server, client, and database components.

---

## How the Schnorr Protocol Works

The Schnorr protocol is a cryptographic system that enables a prover (client) to prove knowledge of a secret to a verifier (server) without revealing the secret itself. Here’s how it works conceptually in this application:

1. **Setup**:
   - The client generates a random secret `s` and computes a public key `y = g^s mod p`, where `g` is the generator and `p` is a large prime number.
   - The public key `y` is shared with the server.

2. **Proof Generation**:
   - The client generates a random value `r` and computes a commitment `t = g^r mod p`.
   - The server computes a challenge `c` based on the file checksum and the commitment `t`.
   - The client computes a response `z = r + c * s mod p` using its secret.

3. **Verification**:
   - The server verifies the proof by recomputing the commitment `t' = g^z * y^(-c) mod p` and checking if it matches the original commitment `t`.

This protocol ensures that:
- The server can validate that the client knows the checksum without learning the actual value.
- The integrity and confidentiality of the file checksum are preserved.

---

## Explanation of the Code

The application is split into two main components: the **server** and the **client**. A SQLite database is used to store file checksums and public keys for verification.

### Server
The server is responsible for handling file uploads, storing data, and verifying proofs. Key features include:

1. **API Endpoints**:
   - `/upload-csv/`: Accepts a file and the client’s public key. It computes the file checksum, stores it along with the public key in the database, and returns a unique identifier.
   - `/verify-proof/`: Accepts a proof from the client and verifies it using the Schnorr protocol.

2. **Database**:
   - A SQLite database is used to store the `unique_id`, `checksum`, and `public_key` for each client. This ensures that multiple clients can interact with the server independently.

3. **Key Methods**:
   - `zkp_server.verify_proof(public_key, checksum, proof)`: Validates the proof provided by the client.
   - `calculate_checksum(file_path)`: Computes the SHA-256 checksum of uploaded files.
   - `save_file(file, unique_id)`: Saves uploaded files in the server's file system.

### Client
The client generates and submits proofs to the server. Key features include:

1. **Workflow**:
   - Computes the SHA-256 checksum of the file to be uploaded.
   - Generates a Schnorr public key and proof.
   - Sends the file and public key to the server via `/upload-csv/`.
   - Submits the proof for verification via `/verify-proof/`.

2. **Key Methods**:
   - `zkp_client.generate_public_key()`: Generates the Schnorr public key.
   - `zkp_client.generate_proof(checksum)`: Generates a proof using the checksum and client’s secret.
   - `upload_file(file_path, public_key)`: Sends the file and public key to the server.
   - `verify_proof(unique_id, proof)`: Sends the proof to the server for verification.

---

## System Architecture and Workflow

The system consists of the following components:
- **Client**: Generates the file checksum, public key, and proof, and interacts with the server.
- **Server**: Handles file uploads, stores client data, and verifies proofs.
- **Database**: Stores checksums and public keys to ensure scalability and support for multiple clients.

### Workflow
1. The client uploads a file and its public key to the server.
2. The server computes the checksum, stores it in the database, and returns a unique identifier.
3. The client generates a Schnorr proof using the file checksum and submits it to the server.
4. The server verifies the proof using the Schnorr protocol.

---

## Future Improvements

1. **Security Enhancements**:
   - Implement SSL/TLS for secure communication between client and server.
   - Add authentication for clients to prevent unauthorized access.

2. **Scalability**:
   - Replace SQLite with a more robust database like PostgreSQL for handling larger datasets.
   - Use a message queue system (e.g., RabbitMQ) for asynchronous proof verification.

3. **User Interface**:
   - Develop a web-based dashboard to upload files and view verification results.

---

## Conclusion

This project demonstrates a practical implementation of the Schnorr protocol for secure file verification. By leveraging Zero-Knowledge Proofs, it ensures data confidentiality and integrity, making it suitable for various real-world applications.

