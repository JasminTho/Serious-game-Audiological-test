README - English
# Serious Game with Playful Elements - Audiological Hearing Test

This program demonstrates a classical hearing test. Based on the results of the hearing test, it is possible to assess whether the patient has a hearing loss.

## Motivation
Hearing loss is a major problem affecting many people. The diagnosis of this condition is done by doctors and audiologists. Hearing loss is, especially in older people, often a gradual process. Additionally, many people face psychological barriers when visiting a doctor. As a result, hearing loss is often diagnosed only when it is already at an advanced stage. As part of my training to become a data scientist, I am learning different skills such as Python, machine learning and SQL. Furthermore, I have gained basic knowledge in audiology through my previous work experience. Based on this, I aim to develop a simple hearing test that patients can use at home. This test includes a basic hearing threshold measurement using standard pure tones. In addition, the test should analyze the speech understanding using the Freiburger one- and two-syllable test. Finally, the program should run through a web interface, so that users can use this tool without installing additional software. The target group includes all individuals who want to check their hearing independently in a low-threshold and accessible manner.

## Implemented functions
- Audiological hearing test in the standard frequencies (125 - 8000 Hz) with increasing sound level.
- The test results are currently displayed on the console. A graphical user interface to display the results as an audiogram is planned.

## Next step
- The program file audio.py will be implemented using an object-oriented approach.
- Implementation of a main.py file, from which all submodules are executed.
- Development of a graphical user interface via Tkinter, using English and German menus.

## Planned functions
- Plot the audiological results as an audiogram.
- Implementation of synthetic test data for training a machine learning algorithm in a database e.g. PostgreSQL or Excel. An option is provided to extend the dataset with free, available, anonymized audiological data.
- Train the machine learning algorithm with the test to detect, based on the test results, whether a participant has a hearing loss.
- Integration of a speech test e.g. the Freiburger one- and two-syllable test.
- Build a level system for the game. The game mechanics are currently in the conceptual phase.
- Build a web application.

## Installation
The program runs on all common operating systems. To start the program, it is necessary to install Python 3.10 or higher.
Additionally, the following modules are necessary:
- numpy
- sounddevice
- threading
- time

## Planned structure of the program
- main.py
  - audio.py
  - speechtest.py
  - freiburger_sentences_eng.py
  - freiburger_sentences_ger.py
  - audiogram.py  
  - data_handler.py 
  - hearing_profiles.py
  - ml_model.py
  - gui_tkinter.py
  - gui_webbased.py                         

## Licence
The program is freely available. Feedback and suggestions are welcome.

## Disclaimer
- Project idea and program code are from myself. The concept of this application is refined with the KI-tool ChatGPT. The project is supervised by a tutor of VelpTec edutainment.
- This program is not a medical diagnosis tool and does not replace professional medical consultation.

-------------------------------------------------------------------------------------------------------------------
<br>
README - German

# Serious Game mit spielerischen Elementen (Gamification) - Audiologischer Hörtest
Dieses Programm zeigt einen klassischen Hörtest. Anhand der Ergebnisse des Hörtests soll der Proband einschätzen, ob ein Hörverlust vorliegt.

## Motivation
Hörverlust ist ein zentrales Problem vieler Menschen. Die Diagnose dieser Funktionsstörung erfolgt durch Ärzte und Audiologen. Ein Hörverlust ist jedoch, gerade bei älteren Patienten oftmals ein schleichender Prozess. Viele Menschen besitzen eine gewisse Hemmschwelle, wenn es darum geht zum Arzt zu gehen. Somit kann es passieren, dass der Hörverlust erst diagnostiziert wird, wenn der Hörverlust bereits weit fortgeschritten ist. Im Rahmen meiner Weiterbildung zum Data Scientist lerne ich u.a. Python, Machine Learning und SQL. Des Weiteren konnte ich in meinen bisherigen Berufserfahrungen Kenntnisse im Bereich der Audiologie sammeln. Mithilfe dieser Kenntnisse möchte ich einen einfachen Hörtest programmieren, den die Patienten schon zu Hause am PC durchführen können. Dieser Test soll zum einen einen einfachen Hörschwellentest mittels standardisierter Töne umfassen. Weitergehend wird das Sprachverstehen mittels Freiburger Einsilber- und Zweisilbertest gemessen. Das Programm soll auf einem Webinterface laufen, damit Patienten es ohne Installation von Programmen verwenden können. Zielgruppe sind alle Personen, die ihr Hörvermögen eigenständig und niedrigschwellig überprüfen möchten.

## Implementierte Funktionen
- Audiologischer Hörtest in den Standardfrequenzen (125 - 8000 Hz) mit Erhöhung des Lautpegels
- Die Ergebnisse werden aktuell in der Konsole ausgegeben. Eine grafische Darstellung als Audiogramm ist geplant.

## Nächste Schritte
- Die Programmdatei audio.py wird objektorientiert programmiert 
- Implementierung einer main.py Datei, von der aus Unterprogramme gestartet werden
- Entwicklung einer Benutzeroberfläche via Tkinter mit englischem und deutschem Menü

## Geplante Funktionen
- Plotten der audiologischen Ergebnisse als Audiogramm
- Implementierung von synthetischen Testdaten zum Trainieren des Machine-Learning-Algorithmus z. B. über PostgreSQL oder Excel, mit der Option zur späteren Erweiterung um frei verfügbare anonymisierte Audiologiedaten.
- Trainieren eines Machine-Learning-Algorithmus, der anhand der Testergebnisse erkennen soll, ob ein Proband an einem Hörverlust leidet 
- Einbettung des Freiburger Ein- und Zweisilber Tests 
- Implementierung eines Levelsystems für das Spiel. Spielmechaniken wie ein Levelsystem sind geplant, befinden sich jedoch noch in der Konzeptionsphase.
- Aufbau in einer Web-Applikation

## Installation
Das Programm läuft auf allen gängigen Betriebssystemen. Zum Starten des Programms wird Python 3.10 oder eine höhere Version benötigt
Zudem sind folgende Module notwendig:
- keyboard
- numpy
- sounddevice
- threading
- time

## Geplanter Aufbau des Programms
- main.py
  - audio.py
  - speechtest.py
  - freiburger_sentences_eng.py
  - freiburger_sentences_ger.py
  - audiogram.py  
  - data_handler.py 
  - hearing_profiles.py
  - ml_model.py
  - gui_tkinter.py
  - gui_webbased.py   

## Lizenz 
Programm ist frei nutzbar. Feedback und Anregungen sind ausdrücklich erwünscht.

## Disclaimer
-	Projektidee und Programmcode stammen von mir, die konzeptionelle Entwicklung wurde mittels des KI-Tools ChatGPT verfeinert. Das Projekt wird von einem Tutor von VelpTec Edutainment betreut.
-	Dieses Projekt stellt kein medizinisches Diagnosetool dar und ersetzt keine fachärztliche Untersuchung oder Beratung.

