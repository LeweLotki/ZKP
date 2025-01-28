# Studio projektowe - raport
### Artur Stefańczyk 406645
### Łukasz Kołodziej indeks

### Jak działa protokół Schnorra?

Protokół Schnorra to jeden z najbardziej znanych protokołów zerowej wiedzy, który pozwala na udowodnienie prawdziwości pewnego stwierdzenia bez ujawniania żadnych dodatkowych informacji poza tym, że stwierdzenie jest prawdziwe. Protokół ten jest szeroko stosowany w kryptografii, zwłaszcza w kontekście dowodów zerowej wiedzy, które są używane do weryfikacji danych bez ujawniania ich zawartości.

W skrócie, protokół Schnorra działa w oparciu o trzy główne etapy:

#### 1. **Ustalenie parametrów publicznych**
W pierwszym kroku protokołu Schnorra, strona udowadniająca (tzw. prover) oraz strona weryfikująca (tzw. verifier) ustalają publiczne parametry, które będą używane w trakcie protokołu. Do tych parametrów należy:
- **Generatory** \(g\) oraz **moduł** \(p\), który jest liczbą pierwszą. Generator \(g\) jest wykorzystywany do generowania wartości, które pozwolą na wygenerowanie dowodu.
  
#### 2. **Generowanie publicznego klucza**
Prover generuje swój **tajny klucz** \(x\) (losowa liczba w obrębie pewnej grupy liczb) oraz oblicza swój **publiczny klucz** \(y\). Publiczny klucz obliczany jest jako:
\[
y = g^x \mod p
\]
Gdzie:
- \(g\) – generator
- \(x\) – tajny klucz
- \(p\) – moduł (liczba pierwsza)

Prover wysyła swój publiczny klucz \(y\) do weryfikującego.

#### 3. **Dowód i wyzwanie**
- **Prover** generuje losową liczbę \(r\) (zwaną "komitmentem"), która jest wykorzystywana w procesie generowania dowodu.
- Na podstawie \(r\), prover oblicza wartość komitmentu \(t = g^r \mod p\) i wysyła ją do weryfikującego.
- Weryfikator generuje **wyzwanie** \(c\), które jest losowo wybraną liczbą (zwykle z zakresu od 0 do pewnej liczby, zależnej od parametrów systemu).
- Prover, mając dostęp do swojego tajnego klucza \(x\) oraz \(r\), oblicza odpowiedź \(s = r + c \cdot x \mod p\).

#### 4. **Weryfikacja dowodu**
Weryfikator otrzymuje parę \((t, s)\), która jest dowodem. Następnie weryfikuje, czy spełniony jest warunek:
\[
g^s \equiv t \cdot y^c \mod p
\]
Jeśli powyższy warunek jest spełniony, wtedy weryfikator uznaje dowód za prawdziwy, co oznacza, że prover zna tajny klucz \(x\) bez jego ujawniania.

#### 5. **Zakończenie**
W przypadku poprawnego przejścia wszystkich etapów weryfikacji, prover udowodnił, że zna tajny klucz \(x\), ale nie ujawnił samego klucza. Protokół Schnorra zapewnia, że nawet w przypadku wielokrotnych powtórzeń procesu, prover nie będzie w stanie manipulować dowodem bez znajomości tajnego klucza.

---

Protokół Schnorra jest uważany za bardzo bezpieczny i efektywny, a jego zastosowanie w kryptografii pozwala na realizację wielu funkcji, takich jak podpisy cyfrowe czy weryfikacja tożsamości w sposób zachowujący prywatność.

### 2. Wprowadzenie do naszego kodu

W tej sekcji przedstawiamy ogólny przegląd tego, co zostało zaimplementowane w projekcie. Nasz kod implementuje protokół Schnorra jako przykład protokołu zerowej wiedzy. W projekcie stworzono zarówno aplikację serwerową, jak i kliencką, które współpracują ze sobą w celu przeprowadzenia procesu weryfikacji dowodów.

#### 2.1. **Struktura projektu**
Projekt składa się z dwóch głównych komponentów:
- **Serwer** – aplikacja odpowiedzialna za obsługę żądań związanych z przesyłaniem plików, weryfikowaniem dowodów oraz przechowywaniem danych (w tym publicznych kluczy i checksum).
- **Klient** – aplikacja, która generuje dowody zgodnie z protokołem Schnorra, wysyła pliki do serwera, a następnie weryfikuje swoje dowody, sprawdzając, czy zostały one poprawnie zweryfikowane przez serwer.

#### 2.2. **Funkcjonalności zaimplementowane w kodzie**
W projekcie zaimplementowano następujące funkcjonalności:

1. **Obliczanie sumy kontrolnej (checksum)**:
   - Klient oblicza sumę kontrolną (SHA-256) dla przesyłanego pliku. Jest to istotna część protokołu, ponieważ suma kontrolna jest wykorzystywana w późniejszych etapach do wygenerowania wyzwań w procesie weryfikacji.

2. **Generowanie klucza publicznego**:
   - Klient generuje publiczny klucz na podstawie swojego tajnego klucza. Klucz publiczny jest wykorzystywany do udowodnienia, że klient zna swój tajny klucz, bez jego ujawniania. Klient wysyła swój publiczny klucz do serwera w celu przechowywania i weryfikacji.

3. **Generowanie dowodu zgodnie z protokołem Schnorra**:
   - Klient generuje dowód na podstawie wygenerowanego publicznego klucza i obliczonej sumy kontrolnej. Dowód składa się z dwóch elementów: komitmentu i odpowiedzi. Komitment jest obliczany na podstawie losowo wybranego \(r\), a odpowiedź \(s\) jest obliczana na podstawie tajnego klucza \(x\) oraz wygenerowanego wyzwania \(c\).

4. **Wysyłanie pliku i klucza publicznego na serwer**:
   - Klient przesyła plik do serwera, jednocześnie wysyłając swój publiczny klucz. Serwer zapisuje plik i klucz, a także oblicza sumę kontrolną przesłanego pliku, aby później użyć jej do weryfikacji.

5. **Weryfikacja dowodu przez serwer**:
   - Po otrzymaniu dowodu, serwer weryfikuje go, sprawdzając, czy spełniony jest odpowiedni warunek matematyczny \( g^s \equiv t \cdot y^c \mod p \), gdzie \(s\) jest odpowiedzią klienta, \(t\) to komitment, a \(y\) to publiczny klucz klienta. Jeśli warunek jest spełniony, dowód jest uznawany za poprawny.

6. **Baza danych i przechowywanie danych**:
   - Serwer przechowuje dane (checksum, publiczne klucze) w bazie danych SQLite. Umożliwia to obsługę wielu klientów, ich danych oraz dowodów na przestrzeni różnych sesji.

#### 2.3. **Technologie użyte w projekcie**
Projekt wykorzystuje następujące technologie:
- **FastAPI** – framework do tworzenia aplikacji webowych, który obsługuje żądania HTTP w serwerze.
- **SQLite** – lekka baza danych do przechowywania danych (w tym publicznych kluczy i checksum) na serwerze.
- **Python** – język programowania, który jest używany do implementacji protokołu oraz aplikacji klienckiej i serwerowej.
- **Docker** – użyty do konteneryzacji aplikacji serwerowej i klienckiej, co ułatwia uruchamianie oraz zarządzanie projektem na różnych środowiskach.

#### 2.4. **Przebieg komunikacji**
Proces komunikacji pomiędzy klientem a serwerem przebiega w kilku krokach:
1. Klient oblicza sumę kontrolną pliku i generuje swój publiczny klucz.
2. Klient wysyła plik i swój publiczny klucz do serwera.
3. Serwer zapisuje plik, oblicza jego checksumę i przechowuje klucz publiczny.
4. Klient generuje dowód na podstawie swojego tajnego klucza i sumy kontrolnej, a następnie wysyła go do serwera.
5. Serwer weryfikuje dowód i zwraca odpowiedź klientowi.

#### 2.5. **Wnioski**
Implementacja protokołu Schnorra w tym projekcie pozwala na bezpieczne udowodnienie, że klient posiada pewne tajne informacje (np. tajny klucz), bez ich ujawniania. Jest to przykład zastosowania protokołów zerowej wiedzy, które znajdują szerokie zastosowanie w kryptografii, zwłaszcza w kontekście anonimowych transakcji i weryfikacji tożsamości.

W kolejnym etapie planujemy rozbudowę systemu, dodanie lepszej obsługi błędów oraz integrację z bardziej rozbudowanymi systemami bazodanowymi, co pozwoli na skalowanie aplikacji i wsparcie wielu użytkowników.

### 3. Jak działa kod: Szczegółowy opis implementacji

W tej sekcji szczegółowo omówimy, jak działa nasz kod i jak poszczególne komponenty współdziałają, aby zaimplementować protokół Schnorra i zapewnić bezpieczeństwo komunikacji między klientem a serwerem. Skupimy się na kluczowych funkcjach i zmiennych, które realizują całą logikę.

#### 3.1. **Struktura projektu**

Projekt składa się z dwóch głównych komponentów:
- **Klient**: Wysyła dowód ZKP i publiczny klucz do serwera, a także generuje sumy kontrolne dla plików.
- **Serwer**: Weryfikuje dowód ZKP oraz przechowuje publiczne klucze i sumy kontrolne w bazie danych SQLite.

Poniżej przedstawiamy szczegóły działania kodu.

#### 3.2. **Klient: Generowanie publicznego klucza i dowodu ZKP**

Kluczowe funkcje w kliencie to `generate_public_key` oraz `generate_proof`.

##### 3.2.1. **Generowanie publicznego klucza**

W funkcji `generate_public_key` generujemy publiczny klucz na podstawie tajnego klucza klienta. Tajny klucz jest losowany w obrębie liczby pierwszej \( p \), a publiczny klucz obliczany jako:

\[
y = g^x \mod p
\]

Gdzie:
- \( g \) to generator,
- \( x \) to tajny klucz klienta,
- \( p \) to liczba pierwsza.

```python
def generate_public_key(self) -> int:
    """Generuje publiczny klucz na podstawie sekretu."""
    return pow(self.generator, self.secret, self.prime)
```

**Zmienne**:
- `self.secret`: Tajny klucz klienta.
- `self.generator`: Generator używany do obliczenia publicznego klucza.
- `self.prime`: Liczba pierwsza wykorzystywana w obliczeniach.

##### 3.2.2. **Generowanie dowodu ZKP**

W funkcji `generate_proof` klient generuje dowód dla podanej sumy kontrolnej. Proces ten obejmuje obliczenie komitmentu, wyzwania i odpowiedzi:

1. Losowanie liczby \( r \), która będzie użyta do obliczenia komitmentu.
2. Obliczenie komitmentu \( t = g^r \mod p \).
3. Obliczenie wyzwania \( c \), które jest funkcją haszującą z sumy kontrolnej i komitmentu.
4. Obliczenie odpowiedzi \( s = r + c \cdot x \mod p \).

```python
def generate_proof(self, checksum: str) -> dict:
    r = secrets.randbelow(self.prime)  # Losowa liczba r
    commitment = pow(self.generator, r, self.prime)  # Komitment: g^r mod p
    challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime  # Wyzwanie
    response = (r + challenge * self.secret) % self.prime  # Odpowiedź

    print(f"Client Proof: r={r}, commitment={commitment % self.prime}, challenge={challenge}, response={response}")
    return {"commitment": commitment, "response": response}
```

**Zmienne**:
- `r`: Losowa liczba wykorzystywana w obliczeniach.
- `commitment`: Komitment obliczany na podstawie \( g^r \mod p \).
- `checksum`: Suma kontrolna, która jest podstawą do generowania wyzwania.
- `challenge`: Wyzwanie obliczane na podstawie sumy kontrolnej i komitmentu.
- `response`: Odpowiedź obliczana na podstawie wyzwania i tajnego klucza.

#### 3.3. **Serwer: Weryfikacja dowodu ZKP**

Serwer weryfikuje poprawność dowodu ZKP, który klient wysyła na serwer. Weryfikacja polega na obliczeniu oczekiwanego komitmentu i porównaniu go z komitmentem przesłanym przez klienta.

```python
def verify_proof(self, public_key: int, checksum: str, proof: dict) -> bool:
    """Weryfikuje dowód Zero-Knowledge Proof."""
    commitment = proof["commitment"] % self.prime
    response = proof["response"] % self.prime
    challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime

    print(f"Server Verification: commitment={commitment}, response={response}, challenge={challenge}")

    try:
        expected_commitment = (
            pow(self.generator, response, self.prime) *
            pow(public_key, self.prime - 1 - challenge, self.prime)  # Modular inverse
        ) % self.prime
        print(f"Expected Commitment: {expected_commitment}")
    except ValueError as e:
        print(f"Error in modular arithmetic: {e}")
        return False

    return commitment == expected_commitment
```

**Zmienne**:
- `commitment`: Komitment, który klient wysyła, a serwer go weryfikuje.
- `response`: Odpowiedź, którą klient przesyła do serwera.
- `challenge`: Wyzwanie obliczane przez serwer.
- `expected_commitment`: Obliczona przez serwer wartość komitmentu, która ma zostać porównana z wartością przesłaną przez klienta.

Serwer oblicza tzw. odwrotność modularną \( y^{-c} \mod p \), co pozwala mu zweryfikować poprawność odpowiedzi. Jeśli obliczony komitment zgadza się z tym, który przesłał klient, wówczas dowód jest uznawany za prawdziwy.

#### 3.4. **Komunikacja pomiędzy klientem a serwerem**

W kodzie klienta, po wygenerowaniu dowodu, ten jest wysyłany do serwera w celu weryfikacji:

```python
def verify_proof(unique_id: str, proof: dict) -> bool:
    """Weryfikuje dowód z serwerem."""
    response = requests.post(
        f"{settings.SERVER_URL}/verify-proof/",
        data={"id": unique_id, "proof": proof}
    )

    if response.status_code == 200:
        print(response.json())
        return True

    print(f"Error verifying proof: {response.text}")
    return False
```

**Działanie**:
- Klient wysyła zapytanie POST na endpoint `/verify-proof/` z ID unikalnym oraz dowodem w postaci komitmentu i odpowiedzi.
- Serwer odbiera zapytanie, weryfikuje dowód, a następnie zwraca odpowiedź.

#### 3.5. **Baza danych**

Na serwerze dane, takie jak klucze publiczne oraz sumy kontrolne przesyłanych plików, są przechowywane w bazie danych SQLite. Serwer używa tego do obsługi wielu klientów, przechowując ich klucze publiczne i sumy kontrolne w tabeli `client_data`.

```python
def save_to_db(unique_id: str, checksum: str, public_key: int):
    """Zapisuje dane do bazy SQLite."""
    db_session = SessionLocal()
    try:
        db_session.execute(
            """
            INSERT INTO client_data (unique_id, checksum, public_key)
            VALUES (?, ?, ?)
            """, (unique_id, checksum, public_key)
        )
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Error saving to DB: {str(e)}")
```

**Działanie**:
- Klient przesyła sumę kontrolną oraz klucz publiczny, które są zapisywane w tabeli `client_data` w bazie danych SQLite.
- W przyszłości dane te mogą być wykorzystywane do weryfikacji dowodów z różnych klientów.

### 4. Użycie Dockera do uruchomienia aplikacji

W tej sekcji opisujemy, jak Docker został użyty do uruchomienia naszej aplikacji oraz jak działa proces uruchamiania zarówno klienta, jak i serwera. Docker zapewnia izolację środowiskową, co pozwala na uruchomienie aplikacji na różnych maszynach bez konieczności instalowania wszystkich zależności na lokalnym systemie.

#### 4.1. **Docker Compose - Automatyzacja uruchamiania serwera i klienta**

Aby uprościć proces uruchamiania aplikacji w kontenerach Docker, wykorzystaliśmy **Docker Compose**. Dzięki niemu możemy zdefiniować usługi w jednym pliku (`docker-compose.yml`), a następnie uruchomić całą aplikację jednym poleceniem.

W projekcie mamy dwa główne kontenery:
- **Serwer**: Odpowiada za weryfikację dowodów oraz przechowywanie danych w bazie SQLite.
- **Klient**: Odpowiada za generowanie dowodów ZKP oraz wysyłanie ich do serwera.

Oto przykładowy plik `docker-compose.yml`:

```yaml
version: '3.8'

services:
  zkp-server:
    build:
      context: ./server
    ports:
      - "8000:8000"
    volumes:
      - ./server:/app
    environment:
      - DATABASE_URL=sqlite:///./test.db
    networks:
      - zkp-network

  zkp-client:
    build:
      context: ./client
    volumes:
      - ./client:/app
    networks:
      - zkp-network
    entrypoint: ["sleep", "infinity"]

networks:
  zkp-network:
    driver: bridge
```

- **Serwer** (usługa `zkp-server`):
  - Jest uruchamiany na porcie `8000`, co pozwala klientowi na komunikację z serwerem przez HTTP.
  - Baza danych SQLite jest przechowywana w katalogu `./server/test.db`.
  - Serwer jest odpowiedzialny za obsługę żądań związanych z weryfikacją dowodów ZKP i przechowywaniem danych.

- **Klient** (usługa `zkp-client`):
  - Klient działa w kontenerze, który nie uruchamia się od razu, dzięki użyciu `entrypoint: ["sleep", "infinity"]`. Dzięki temu możemy ręcznie uruchomić klienta w kontenerze po uruchomieniu serwera.
  - Klient wstrzymuje swoje działanie, czekając na ręczne wywołanie polecenia z zewnątrz.

#### 4.2. **Budowanie i uruchamianie kontenerów Docker**

Aby uruchomić projekt, wystarczy uruchomić następujące polecenia:

1. **Uruchomienie usług w tle (detached mode)**:
   
   Uruchom polecenie Docker Compose, aby uruchomić serwer i klienta w kontenerach:

   ```bash
   docker compose up --build -d
   ```

   Parametr `--build` spowoduje ponowne zbudowanie obrazów kontenerów, jeśli zajdą jakiekolwiek zmiany w plikach. Parametr `-d` uruchomi kontenery w tle (detached mode), aby nie blokowały terminala.

2. **Sprawdzenie statusu kontenerów**:

   Możesz sprawdzić, czy kontenery zostały uruchomione poprawnie, używając polecenia:

   ```bash
   docker ps
   ```

   Powinno to wyświetlić listę działających kontenerów, gdzie znajdziesz kontener serwera (`zkp-server`) działający na porcie `8000`, oraz kontener klienta (`zkp-client`), który będzie wstrzymany (`sleep infinity`).

#### 4.3. **Interakcja z kontenerem klienta**

Aby uruchomić klienta po uruchomieniu serwera, użyj polecenia `docker exec`:

1. **Wejdź do kontenera klienta**:

   Użyj poniższego polecenia, aby wejść do kontenera klienta i uruchomić aplikację:

   ```bash
   docker exec -it zkp-client-1 python -m app.main
   ```

   - `zkp-client-1` to nazwa kontenera klienta, która może różnić się w zależności od konfiguracji.
   - `python -m app.main` uruchamia główny moduł aplikacji, w którym zawarta jest logika generowania dowodu ZKP i komunikacji z serwerem.

2. **Ręczne uruchamianie aplikacji**:

   W przypadku, gdy kontener klienta nie uruchamia się automatycznie, po użyciu powyższego polecenia, program na kliencie wykona swoje zadanie – wygeneruje publiczny klucz, wyśle plik na serwer oraz wyśle dowód do weryfikacji.

#### 4.4. **Monitorowanie i debugowanie**

W przypadku, gdy napotkasz jakiekolwiek problemy podczas działania aplikacji, możesz sprawdzić logi kontenera serwera i klienta:

- **Logi serwera**:

  Aby sprawdzić logi serwera, użyj poniższego polecenia:

  ```bash
  docker logs zkp-server-1
  ```

- **Logi klienta**:

  Aby sprawdzić logi klienta, użyj poniższego polecenia:

  ```bash
  docker logs zkp-client-1
  ```

Możesz używać tych logów, aby śledzić, co dzieje się w danym momencie, oraz zdiagnozować wszelkie błędy lub problemy.
