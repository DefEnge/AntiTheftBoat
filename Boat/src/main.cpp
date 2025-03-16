#include <iot_board.h>
#include <ESPAsyncWebServer.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <Preferences.h>
#include <DNSServer.h> 
#include <esp_wifi.h>
#include <ArduinoJson.h>
#include <HTTPClient.h> 
#include <WiFiClient.h>
//For Lora
const char *devEui = ""; 
const char *appEui = "0000000000000000";
const char *appKey = "";
char myStr[50];
char outStr[255];
String wifiOpt="";
byte recvStatus = 0;
int count_sent = 0;
bool configMode = false;
String targa = "";
String devui = "";
String ssid = "";
String password = "";
Preferences preferences;
boolean runEvery(unsigned long interval)
{
 static unsigned long previousMillis = 0;
 unsigned long currentMillis = millis();
 if (currentMillis - previousMillis >= interval)
 {
   previousMillis = currentMillis;
   return true;
 }
 return false;
}
void onLoRaReceive (sBuffer *Data_Rx, bool isConfirmed, uint8_t fPort){
  String s = String((char *) Data_Rx->Data, HEX);
  Serial.println(s);
}
//end lora
int httpPort=5000;
const char* host = "";
const char* url = "/register/";
WiFiClient client;
void fetchDeviceData() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.setTimeout(20000); // Imposta un timeout di 10 secondi
    http.begin("");  // URL del server
    http.addHeader("Content-Type", "application/json");
    Serial.println("Inizio richiesta POST");
    // Creazione del JSON
    StaticJsonDocument<256> jsonDoc;
    preferences.begin("user_config",false);
    jsonDoc["deviceId"] = preferences.getString("deviceId", "");
    jsonDoc["nome"] = preferences.getString("nome", "");
    jsonDoc["cognome"] = preferences.getString("cognome", "");
    jsonDoc["targa"] = preferences.getString("targa", "");
    preferences.end();
    String requestBody;
    serializeJson(jsonDoc, requestBody);

    Serial.println(requestBody);
    int httpResponseCode = http.POST(requestBody);
    String response;
    if (httpResponseCode > 0) {
      response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
      if (httpResponseCode == 201){
        http.end();
        preferences.begin("user_config",false);
        preferences.putBool("setup",false);
        preferences.end();
        ESP.restart();
      }
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
      display->clearDisplay();
      display->println(response);
      display->display();
    }
    http.end();
  } else {
    Serial.println("WiFi non connesso, impossibile inviare la richiesta.");
    display->clearDisplay();
    display->println("WiFi non connesso, impossibile inviare la richiesta.");
    display->display();
  }
}
bool connectToWiFi(const char* ssid, const char* password, int timeout = 15000) {
    Serial.print("Connessione a WiFi: ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);  // Avvia la connessione

    unsigned long startAttemptTime = millis();

    // Attendi la connessione con un timeout
    while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < timeout) {
        Serial.print(".");
        delay(1000);
    }

    // Verifica se la connessione è riuscita
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi Connesso!");
        Serial.print("IP Assegnato: ");
        Serial.println(WiFi.localIP());

    // Effettua la richiesta HTTP e processa la risposta
    
        return true;  // Connessione riuscita
    } else {
        Serial.println("\nErrore di connessione!");
        return false;  // Timeout o errore
    }
}

unsigned long pressStartTime = 0;
bool isPressed = false;
void IRAM_ATTR onBtnReleased();
void startConfigMode();
void IRAM_ATTR onBtnPressed() {
  if (!isPressed) {  
      pressStartTime = millis();  // Salva il tempo di inizio pressione
      isPressed = true;
      detachInterrupt(BTN_1);
      attachInterrupt(BTN_1, onBtnReleased, RISING);
  }
}

void IRAM_ATTR onBtnReleased() {
  if (isPressed) { // Only process if a press was registered
    unsigned long pressDuration = millis() - pressStartTime;
    isPressed = false;
    Serial.println("fino a qua si");
    if (pressDuration >= 5000) {
      //se sono qui, ho tenuto il mio bottone premuto per 5 fucking secondi.
      //startConfigMode();
      preferences.begin("user_config", false);
      preferences.putBool("setup",true);
      preferences.end();
      delay(3000);
      Serial.println("riavvio per fare la configurazione");
      ESP.restart();
    }
    detachInterrupt(BTN_1);
    attachInterrupt(BTN_1, onBtnPressed, FALLING);
  }
}




const char configPage[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form di Registrazione</title>
    <style>
        body {
            font-family: sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }

        .form-container {
            width: 400px;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        h2 {
            color: #333;
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            text-align: left;
        }

        input[type="text"], input[type="password"], select {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }

        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }

        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Registrazione Dispositivo</h2>
        <form action="/save" method="post">
            <label for="ssid">SSID della rete Wi-Fi:</label>
            <select id="ssid" name="ssid" required>
                %WIFI_OPTIONS%
            </select>

            <label for="password">Password Wi-Fi:</label>
            <input type="password" id="password" name="password" required>

            <label for="targa">Targa:</label>
            <input type="text" id="targa" name="targa" required>

            <label for="deviceId">Device ID:</label>
            <input type="text" id="deviceId" name="deviceId" required>

            <label for="nome">Nome:</label>
            <input type="text" id="nome" name="nome" required>

            <label for="cognome">Cognome:</label>
            <input type="text" id="cognome" name="cognome" required>

            <input type="submit" value="Invia">
        </form>
    </div>
</body>
</html>

)rawliteral";
String scanWiFiNetworks() {
  int j=0,n=0;
  while(j<10 && n==0){
    n = WiFi.scanNetworks();
    j++;
    delay(1000);
  } 
  Serial.println("Ho fatto"+String(j)+"cicli, ho trovato "+String(n)+" reti");
  String wifiOptions = "";
  if (n == 0) {
    wifiOptions = "<option value=\"\">No networks found</option>";
  } else {
    for (int i = 0; i < n; ++i) {
      wifiOptions += "<option value=\"" + WiFi.SSID(i) + "\">" + WiFi.SSID(i) + "</option>";
    }
  }
  return wifiOptions;
}
AsyncWebServer server(80);
DNSServer dnsServer; 
bool wificonnesso=false;


  const IPAddress localIP(1,1,1,1);		   // the IP address the web server, Samsung requires the IP to be in public space
  const IPAddress gatewayIP(1,1,1,1);		   // IP address of the network should be the same as the local IP for captive portals
  const IPAddress subnetMask(255, 255, 255, 0);  // no need to change: https://avinetworks.com/glossary/subnet-mask/
  const String localIPURL = "http://1.1.1.1";
  String wifiOptions="";
  void setUpDNSServer(DNSServer &dnsServer, const IPAddress &localIP) {
    #define DNS_INTERVAL 30
      dnsServer.setTTL(3600);
      dnsServer.start(53, "*", localIP);
    }
void startConfigMode() {
  delay(5000);
	WiFi.mode(WIFI_MODE_AP);
	const IPAddress subnetMask(255, 255, 255, 0);
	WiFi.softAPConfig(localIP, gatewayIP, subnetMask);
	WiFi.softAP("ESP32_Config");
  esp_wifi_stop();
	esp_wifi_deinit();
	wifi_init_config_t my_config = WIFI_INIT_CONFIG_DEFAULT();
	my_config.ampdu_rx_enable = false;
	esp_wifi_init(&my_config);
  vTaskDelay(100 / portTICK_PERIOD_MS); 
	esp_wifi_start();
  Serial.println("Access Point Creato: ESP32_Config");
  IPAddress myIP = WiFi.softAPIP();
  wifiOpt=scanWiFiNetworks();
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    
    String html = FPSTR(configPage);
        String htmlCopy = String(html); // Make a copy in RAM
    html.replace("%WIFI_OPTIONS%", wifiOpt);

    request->send(200, "text/html", html);
  });

  server.on("/save", HTTP_POST, [](AsyncWebServerRequest *request) {
    if (request->hasParam("ssid", true) && request->hasParam("password", true) &&
        request->hasParam("targa", true) && request->hasParam("deviceId", true) &&
        request->hasParam("nome", true) && request->hasParam("cognome", true)) {
      
      String ssid = request->getParam("ssid", true)->value();
      String password = request->getParam("password", true)->value();
      String targa = request->getParam("targa", true)->value();
      String deviceId = request->getParam("deviceId", true)->value();
      String nome = request->getParam("nome", true)->value();
      String cognome = request->getParam("cognome", true)->value();
      Serial.println(targa+" "+deviceId+" "+nome+" "+cognome);
      preferences.begin("user_config", false);
      preferences.putString("ssid", ssid);
      preferences.putString("password", password);
      preferences.putString("targa", targa);
      preferences.putString("deviceId", deviceId);
      preferences.putString("nome", nome);
      preferences.putString("cognome", cognome);
      preferences.putBool("setup", false); // Configurazione completata
      preferences.end();
      wificonnesso=connectToWiFi(ssid.c_str(), password.c_str());
      request->send(200, "text/html", "Dati salvati. Riavvia il dispositivo.");
      
    } else {
      request->send(400, "text/plain", "Dati non validi.");
    }
  });
	server.onNotFound([](AsyncWebServerRequest *request) {
		if (request->url() != "/") {  
      request->redirect(localIPURL);
  } else {
      request->send(200, "text/html", configPage);
  }
	});

  setUpDNSServer(dnsServer, localIP);
  server.begin();
}


void setup() {
  IoTBoard::init_buttons();
  IoTBoard::init_serial();
  IoTBoard::init_display();
  pinMode(BTN_1, INPUT_PULLUP);
  attachInterrupt(BTN_1, onBtnPressed, FALLING);  
  preferences.begin("user_config", false);
  targa = preferences.getString("targa", "");
  configMode=preferences.getBool("setup",true);
  devEui=preferences.getString("devui","").c_str();
  devui=preferences.getString("devui","").c_str();
  appKey=preferences.getString("AppKey","").c_str();
  preferences.end();
  Serial.println("Modalità Configurazione");
  if(configMode){
    display->println("Modalità Configurazione");
    display->display();
    startConfigMode();
  } 
  else{
    Serial.println("Modalità Operativa");
    display->clearDisplay();
    display->println("Modalità operativa");
    display->display();
    //no config needed , setting up Lora
    if (IoTBoard::init_lorawan()) {
      lorawan->setDeviceClass(CLASS_A);
      lorawan->setDataRate(SF9BW125);
      // set channel to random
      lorawan->setChannel(MULTI);
      lorawan->setDevEUI(devEui);
      lorawan->setAppEUI(appEui);
      lorawan->setAppKey(appKey);
      lorawan->onMessage(&onLoRaReceive);
      // Join procedure
      bool isJoined;
      do {
        Serial.println("Joining...");
        isJoined = lorawan->join();
  
        // wait for 10s to try again
        delay(10000);
      } while (!isJoined);
      Serial.println("Joined to network");
  
    } else {
      Serial.println("Error");
    }
  }
}

void loop() {
  if(wificonnesso){
    fetchDeviceData();
    wificonnesso=false;
  }
  if(configMode){
    dnsServer.processNextRequest();
    delay(DNS_INTERVAL);
  }else{
    
    //if (runEvery(10000)) {
      //Send data with Lora
      /*sprintf(myStr, "Hello-%d", count_sent);
      lorawan->sendUplink(myStr, strlen(myStr), 1, 2);
      count_sent++;*/
    //}
    //lorawan->readData(outStr);
    // Check Lora RX
    //lorawan->update();
  }
  //preferences.begin("user_config", false);
  //Serial.println("Targa: " + preferences.getString("targa", ""));
  //Serial.println("AppKey: " + preferences.getString("AppKey", ""));
  //Serial.println("deveui: " + preferences.getString("devEui", ""));
  //Serial.println("deviceid: " + preferences.getString("DeviceId", ""));
  //preferences.end();
  //delay(3000);
  
}

