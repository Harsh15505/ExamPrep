# Unit 3 & 4: Comprehensive Viva & Theory Questions

This document contains 100 detailed viva and theory questions extracted from the provided lectures on Cyber Security Terminology, DoS/DDoS, IDS/Firewalls, Software Vulnerabilities, and Security at the Application, Transport, and Network Layers.

---

## Part 1: Cyber Security Terminology & Malware (Q1 - Q15)

**Q1: What is a threat in cyber security?**
*Answer:* A threat is any potential danger to information or systems that can result in unauthorized access, data theft, corruption, or service disruption.

**Q2: Differentiate between Passive and Active threats.**
*Answer:* Passive threats involve eavesdropping or monitoring without altering data (e.g., traffic analysis), while Active threats attempt to alter system resources or affect operations (e.g., modification, DoS).

**Q3: Provide examples of natural, human, and environmental threats.**
*Answer:* Natural: Earthquakes, floods. Human: Hacking, phishing. Environmental: Power failure, system overheating.

**Q4: What is a computer virus?**
*Answer:* A computer virus is malicious code that attaches to legitimate files and requires a host file and user interaction to replicate and execute.

**Q5: How does a worm differ from a virus?**
*Answer:* A worm is a standalone malicious program that replicates itself to spread across networks without requiring a host file or user interaction.

**Q6: Give an example of a famous worm.**
*Answer:* The ILOVEYOU Worm and WannaCry Ransomware Worm.

**Q7: What is a Trojan Horse?**
*Answer:* Malware disguised as legitimate software to trick users into executing it.

**Q8: Define Spyware and its purpose.**
*Answer:* Spyware is malware that secretly monitors user activity to steal sensitive information.

**Q9: What is Ransomware?**
*Answer:* Malware that locks files or systems and demands a ransom payment to restore access.

**Q10: How does a rootkit operate?**
*Answer:* It gains administrator-level (root) access while simultaneously hiding its malicious processes from the operating system.

**Q11: What is an intruder in network security?**
*Answer:* An individual or program that attempts to gain unauthorized access to systems or data.

**Q12: Describe a Masquerader intruder.**
*Answer:* An intruder (usually an outsider) who pretends to be an authorized user to gain access.

**Q13: What is a Misfeasor?**
*Answer:* Also known as an Insider Attack, it is an authorized user who misuses their legitimate access privileges.

**Q14: Define a Clandestine User.**
*Answer:* An intruder who gains supervisory (root/admin) control without authorization to evade auditing and access controls.

**Q15: List three common attack techniques used by intruders.**
*Answer:* Password cracking, privilege escalation, and spoofing/impersonation.

---

## Part 2: DoS and DDoS Attacks (Q16 - Q30)

**Q16: What is a Denial of Service (DoS) attack?**
*Answer:* An attack where a single machine floods a server or network with traffic to overload resources, making it unavailable to legitimate users.

**Q17: What is a Distributed Denial of Service (DDoS) attack?**
*Answer:* An attack that overwhelms a system with traffic from multiple distributed sources simultaneously.

**Q18: How does DDoS differ from DoS in terms of origin?**
*Answer:* A DoS attack originates from a single source machine, while a DDoS attack originates from thousands of compromised machines distributed globally.

**Q19: What is a Botnet and how is it used in DDoS?**
*Answer:* A botnet is a network of compromised systems (zombies) controlled by an attacker to launch massive, coordinated traffic toward a target.

**Q20: What are the consequences of a DDoS attack?**
*Answer:* System downtime, financial loss, and severe service unavailability for legitimate users.

**Q21: What is a Volume-based DDoS attack?**
*Answer:* An attack that aims to consume the entire bandwidth of the target network.

**Q22: Give an example of a Volume-based attack.**
*Answer:* UDP floods.

**Q23: What is a Protocol DDoS attack?**
*Answer:* An attack that exploits server resources and network infrastructure protocols rather than bandwidth.

**Q24: Provide an example of a Protocol attack.**
*Answer:* SYN floods.

**Q25: Describe an Application-layer DDoS attack.**
*Answer:* An attack that targets specific web applications by sending seemingly legitimate but highly resource-intensive requests to crash the web server.

**Q26: Give an example of an Application-layer attack.**
*Answer:* HTTP GET/POST floods.

**Q27: Why are file-encrypting software tools classified as an Active Threat?**
*Answer:* Because they actively alter system resources (encrypting files) rather than just passively observing data.

**Q28: How does rate limiting help in DDoS prevention?**
*Answer:* It restricts the number of requests a server accepts from a single IP over a timeframe, preventing attackers from overwhelming the server.

**Q29: What is the role of traffic scrubbing services?**
*Answer:* They analyze incoming traffic, filter out malicious DDoS packets, and only forward clean, legitimate traffic to the target server.

**Q30: How do load balancing and redundancy mitigate DDoS?**
*Answer:* By distributing traffic across multiple servers, preventing any single server from becoming a bottleneck during an attack.

---

## Part 3: IDS, Malware Detection, and Firewalls (Q31 - Q55)

**Q31: What is an Intrusion Detection System (IDS)?**
*Answer:* A security system designed to monitor network traffic, logs, and behaviors to detect and respond to potential threats and unauthorized access.

**Q32: What are the primary objectives of an IDS?**
*Answer:* Detect unauthorized access, monitor for malicious activity, generate alerts, log events, and prevent/limit damage.

**Q33: Describe a Network-based IDS (NIDS).**
*Answer:* An IDS placed at strategic network points to monitor inbound and outbound network traffic for suspicious activities.

**Q34: What kind of attacks is NIDS ideal for detecting?**
*Answer:* DoS attacks, port scanning, and buffer overflow attacks over the network.

**Q35: What is a Host-based IDS (HIDS)?**
*Answer:* An IDS that monitors activities and events on a single specific host (e.g., server or workstation).

**Q36: When is HIDS more effective than NIDS?**
*Answer:* When detecting attacks that bypass network defenses, such as rootkits, privilege escalation, or encrypted malicious traffic.

**Q37: Explain Signature-based detection in IDS.**
*Answer:* It compares incoming traffic patterns to a database of known attack signatures (like an antivirus).

**Q38: What is the main limitation of Signature-based detection?**
*Answer:* It cannot detect new, unknown attacks or zero-day vulnerabilities since no signature exists for them yet.

**Q39: Explain Anomaly-based detection.**
*Answer:* It establishes a baseline of normal behavior and flags any significant deviations (like sudden traffic spikes) as potential attacks.

**Q40: What is a common drawback of Anomaly-based detection?**
*Answer:* It often produces high false-positive rates if legitimate traffic suddenly spikes or normal behavior changes.

**Q41: What is Hybrid Detection?**
*Answer:* Combining both signature-based and anomaly-based methods for better coverage of both known and unknown threats.

**Q42: Name three IDS response mechanisms.**
*Answer:* Alerting (sending notifications), Logging (recording events), and Active Responses (automatically blocking attacks).

**Q43: What is Malware?**
*Answer:* Malicious software designed to damage, disrupt, or gain unauthorized access to computer systems.

**Q44: Explain Behavioral-based malware detection.**
*Answer:* It monitors a program's execution behavior (e.g., file system changes, network activity) rather than its static code signature.

**Q45: What is Sandbox Analysis?**
*Answer:* Running suspicious programs in a secure, isolated environment to observe if their behavior is malicious before allowing them on the real system.

**Q46: Contrast Signature-based and Heuristic-based malware detection.**
*Answer:* Signature-based relies on exact code matches of known malware. Heuristic-based looks for general suspicious patterns and commands, allowing it to catch new variants.

**Q47: What are two key malware prevention techniques?**
*Answer:* Antivirus/Antimalware software installations and rigorous User Education (avoiding phishing links).

**Q48: Define a Firewall.**
*Answer:* A network security system that serves as a barrier, monitoring and controlling incoming and outgoing traffic based on predefined security rules.

**Q49: What is a Packet Filtering Firewall?**
*Answer:* A basic firewall that inspects individual data packets based on IP address, port number, and protocol rules.

**Q50: What is a Stateful Inspection Firewall?**
*Answer:* A firewall that tracks the state of active connections, ensuring incoming packets belong to a valid, established session.

**Q51: How does Stateful Inspection improve over Packet Filtering?**
*Answer:* It maintains state tables, making it much harder for attackers to spoof packets since isolated, out-of-state packets are immediately dropped.

**Q52: What is a Proxy Firewall?**
*Answer:* An application-level firewall that acts as an intermediary, intercepting client requests to inspect application-layer traffic before forwarding it to the server.

**Q53: Describe Next-Generation Firewalls (NGFW).**
*Answer:* Firewalls that integrate stateful inspection, Deep Packet Inspection (DPI), and Intrusion Prevention Systems (IPS) for advanced analysis.

**Q54: What is a Web Application Firewall (WAF)?**
*Answer:* A specialized firewall designed to protect web applications from layer 7 attacks like SQL injection and XSS.

**Q55: What is Deep Packet Inspection (DPI)?**
*Answer:* Examining the actual payload of the packet (the data) rather than just the header information to detect malicious content.

---

## Part 4: Software Vulnerabilities (Q56 - Q80)

**Q56: What is a software vulnerability?**
*Answer:* A flaw, weakness, or bug in software that attackers can exploit to gain unauthorized access or compromise a system.

**Q57: Name four common types of software vulnerabilities.**
*Answer:* Buffer Overflow, SQL Injection, Cross-Site Scripting (XSS), and Zero-Day Exploits.

**Q58: What is a Buffer Overflow?**
*Answer:* It occurs when a program writes more data to a fixed-size memory buffer than it can hold, overflowing into adjacent memory.

**Q59: How does a Buffer Overflow attack work?**
*Answer:* The excess input overwrites boundaries, allowing attackers to change return addresses to execute injected malicious code.

**Q60: What are the potential impacts of a Buffer Overflow?**
*Answer:* Arbitrary Code Execution, system crashes, and data corruption (e.g., the 1988 Morris Worm).

**Q61: Name a mitigation strategy for Buffer Overflow.**
*Answer:* Strict input validation and using secure functions (e.g., using `fgets()` instead of the unsafe `gets()` in C).

**Q62: What is a stack canary?**
*Answer:* A security mechanism that places a known value on the stack before the return pointer; if a buffer overflow alters it, the program halts before executing malicious code.

**Q63: What is a SQL Injection vulnerability?**
*Answer:* A flaw allowing attackers to inject malicious SQL queries into database engines through unsanitized user inputs.

**Q64: How do attackers exploit SQL Injection?**
*Answer:* By altering queries, they can bypass authentication, retrieve hidden data, or delete entire database tables.

**Q65: Provide an example of a common SQL Injection payload.**
*Answer:* `" ' OR '1'='1 "` which forces the database query to evaluate to true, granting unauthorized access.

**Q66: Name two mitigation strategies for SQL Injection.**
*Answer:* Using Parameterized Queries (Prepared Statements) and validating/sanitizing all user inputs.

**Q67: What is an ORM and how does it prevent SQL Injection?**
*Answer:* Object-Relational Mapping (ORM) abstracts database interactions into code objects, preventing developers from manually concatenating unsafe SQL strings.

**Q68: What is Cross-Site Scripting (XSS)?**
*Answer:* A vulnerability where attackers inject malicious JavaScript into web pages viewed by other users.

**Q69: How does XSS work?**
*Answer:* The malicious script executes inside the victim’s browser, compromising their session because the browser trusts the source website.

**Q70: Differentiate between Stored XSS and Reflected XSS.**
*Answer:* Stored XSS permanently saves the payload on the server (e.g., in a comment section). Reflected XSS requires the victim to click a crafted link that bounces the payload off the server back to them.

**Q71: What is DOM-based XSS?**
*Answer:* A vulnerability existing entirely in client-side JavaScript, where the malicious script executes when the browser manipulates the Document Object Model (DOM).

**Q72: What is session hijacking in the context of XSS?**
*Answer:* Using injected JavaScript to steal a user's session cookies and sending them to the attacker, allowing account takeover.

**Q73: How can XSS be mitigated?**
*Answer:* Through strict Output Encoding (escaping special HTML characters) and Input Validation.

**Q74: What is a Content Security Policy (CSP)?**
*Answer:* A browser security mechanism that restricts which external resources (like scripts) are allowed to load and execute on a webpage.

**Q75: Define a Zero-Day Exploit.**
*Answer:* An attack that targets a software vulnerability unknown to the vendor, meaning no patch currently exists.

**Q76: Why are Zero-Day exploits particularly dangerous?**
*Answer:* Because defenses cannot rely on signatures or patches, allowing widespread attacks with little initial resistance.

**Q77: Give a real-world example of a Zero-Day exploit.**
*Answer:* Stuxnet (2010), which leveraged multiple zero-days to target industrial control systems in nuclear facilities.

**Q78: What constitutes Weak Authentication?**
*Answer:* Using default passwords, lacking Multi-Factor Authentication (MFA), or storing credentials insecurely (in plain text).

**Q79: What is credential stuffing?**
*Answer:* An attack where hackers use lists of compromised passwords from one breach to try and access accounts on other platforms.

**Q80: How can weak authentication be mitigated?**
*Answer:* Enforcing minimum password complexity, implementing MFA, and securely hashing/salting passwords in databases.

---

## Part 5: Security at ATN (Application, Transport, Network) Layers (Q81 - Q100)

**Q81: Why is Application Layer security needed?**
*Answer:* It's the most exposed layer to the internet with direct end-user interaction, making it highly susceptible to exploitation via inputs.

**Q82: What kind of data is typically handled at the application layer?**
*Answer:* Highly sensitive personal, financial, and confidential data like login credentials and credit card info.

**Q83: Name three common attacks targeting the application layer.**
*Answer:* SQL Injection, Cross-Site Scripting (XSS), and Remote Code Execution.

**Q84: How does session management relate to application layer security?**
*Answer:* Secure session handling (e.g., using HttpOnly cookies or JWT tokens) is vital to prevent session hijacking and fixation.

**Q85: List three protocols/techniques used for Application Layer security.**
*Answer:* HTTPS, S/MIME, PGP, OAuth, and App-layer firewalls.

**Q86: Why is Transport Layer security needed?**
*Answer:* To provide data privacy and confidentiality by encrypting data in transit, ensuring it cannot be read if intercepted.

**Q87: How does TLS protect against Man-in-the-Middle (MITM) attacks?**
*Answer:* It uses digital certificates and cryptographic handshakes to verify identities and establish a trusted, encrypted tunnel.

**Q88: What ensures Data Integrity at the transport layer?**
*Answer:* Cryptographic Message Authentication Codes (MACs) and hash functions, which detect if data was altered during transmission.

**Q89: How does the transport layer authenticate communicating parties?**
*Answer:* Using public key infrastructure (PKI) and digital certificates to prevent spoofing.

**Q90: What is the relationship between Application and Transport layer security?**
*Answer:* Application protocols (like HTTP and FTP) rely on Transport protocols (like TLS) to provide the encrypted foundation (forming HTTPS, FTPS).

**Q91: Name the primary protocol used for Transport Layer security.**
*Answer:* TLS (Transport Layer Security), which replaced the deprecated SSL.

**Q92: Why is Network Layer security necessary?**
*Answer:* It is the foundation of data transmission (addressing and routing); if compromised, attackers can misroute or intercept entire data traffic flows.

**Q93: Give two examples of packet-based attacks at the network layer.**
*Answer:* IP Spoofing, Packet Sniffing, and Route Hijacking.

**Q94: Are IP packets encrypted by default?**
*Answer:* No, by default, IP packets are sent in plain text and are vulnerable in transit unless secured.

**Q95: What technology is commonly used to secure network layer communications?**
*Answer:* IPsec (Internet Protocol Security) and VPNs (Virtual Private Networks).

**Q96: How does network layer security protect routing integrity?**
*Answer:* It prevents attackers from altering routing tables or performing route hijacking by enforcing secure routing protocols.

**Q97: What is IP Spoofing?**
*Answer:* Forging the source IP address in a packet header to conceal the sender's identity or impersonate another computing system.

**Q98: What is packet sniffing?**
*Answer:* The unauthorized interception and logging of data packets traversing a network.

**Q99: Name three benefits of Network Layer Security.**
*Answer:* Confirms data integrity at the routing level, prevents packet tampering, and supports secure site-to-site enterprise VPNs.

**Q100: How does a VPN secure communication over untrusted networks?**
*Answer:* It creates an encrypted, secure tunnel over public networks (like public Wi-Fi), protecting data from snoopers and MITM attacks at the network layer.
