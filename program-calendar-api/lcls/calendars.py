from dataclasses import dataclass

@dataclass
class Calendar:
    name: str
    id: str
    line: str | None
    machine: str
    hutch: str | None
    is_program: bool

all_calendars = [
            Calendar(name="NC-MD-FEEH",  id="ndq2se9gtt6paqki65scp9k8ek@group.calendar.google.com", line="HXR", machine="NC", hutch=None, is_program=True),
            Calendar(name="NC-MD-FEES",  id="ealpkrkimh4g4mgp4vc637gfqg@group.calendar.google.com", line="SXR", machine="NC", hutch=None, is_program=True),
            Calendar(name="NC-XRT",      id="j98e97c6g7lgno3ahrm361g1dc@group.calendar.google.com", line="HXR", machine="NC", hutch=None, is_program=True),
            Calendar(name="NC-TMO",      id="tauubmn9n6evkir835i4uqde3c@group.calendar.google.com", line="SXR", machine="NC", hutch="TMO", is_program=True),
            Calendar(name="NC-ChemRIXS", id="rf402b8ts02ultfjc62l8clalk@group.calendar.google.com", line="SXR", machine="NC", hutch="ChemRIXS", is_program=True),
            Calendar(name="NC-qRIXS",    id="qbbeu264618gah7l28kqiq84r8@group.calendar.google.com", line="SXR", machine="NC", hutch="qRIXS", is_program=True),
            Calendar(name="NC-TXI",      id="ag90tn65tk169kgpkt8i7286ns@group.calendar.google.com", line="SXR", machine="NC", hutch="TXI", is_program=True),
            Calendar(name="NC-XPP",      id="6sr414nehbugn2k67efq71mppg@group.calendar.google.com", line="HXR", machine="NC", hutch="XPP", is_program=True),
            Calendar(name="NC-XCS",      id="ljjr3de15ianjh42ahlqvcv5s4@group.calendar.google.com", line="HXR", machine="NC", hutch="XCS", is_program=True),
            Calendar(name="NC-MFX",      id="lun28fjakluvivt5q4fj6qu2eg@group.calendar.google.com", line="HXR", machine="NC", hutch="MFX", is_program=True),
            Calendar(name="NC-CXI",      id="lt8askfj7kivnsfki1dgc63ifs@group.calendar.google.com", line="HXR", machine="NC", hutch="CXI", is_program=True),
            Calendar(name="NC-MEC",      id="nka5r8ffmrik5jcdih8nu73r1k@group.calendar.google.com", line="HXR", machine="NC", hutch="MEC", is_program=True),
            Calendar(name="NC-PAMM",     id="o76php9rppejapugsk0g9fffes@group.calendar.google.com", line=None,  machine="NC", hutch=None, is_program=True),
            Calendar(name="SC Linac MD", id="go9dvt2fj9g6951qvip05pbi30@group.calendar.google.com", line=None,  machine="SC", hutch=None, is_program=True),
            Calendar(name="SC-PAMM", id="abf581b324438d82623b89ca3be37a541ce1d67d2148b578b3dfefbac417b2a1@group.calendar.google.com", line=None, machine="SC", hutch=None, is_program=True),
            Calendar(name="SC-MD-FEES", id="4edfcc9b959034909ac9035917482370c007b28dceacb6edd9c9223f0f944a6e@group.calendar.google.com", line="SXR", machine="SC", hutch=None, is_program=True),
            Calendar(name="SC-MD-FEEH", id="266ac5957019dc9018cb2a27462d97029787edde0a0c3c7f4bb9d1434fa6b417@group.calendar.google.com", line="HXR", machine="SC", hutch=None, is_program=True),
            Calendar(name="SRF Comm", id="nq7j43ttbr66pe871r2emgfor0@group.calendar.google.com", line=None, machine="SC", hutch=None, is_program=False),
            Calendar(name="SC-ChemRIXS", id="0e4eed830248da6cfb26ee3c734bdbfa4b482647bc828992547c4c8f5de51d46@group.calendar.google.com", line="SXR", machine="SC", hutch="ChemRIXS", is_program=True),
            Calendar(name="SC-TMO",      id="e8c51288aa6fe89c7304f665e4ff54240059b52c0f2241d0dbde91399f562f33@group.calendar.google.com", line="SXR", machine="SC", hutch="TMO", is_program=True),
            Calendar(name="SC-qRIXS",    id="a926446f7df37ebc0ff9ddc4cf09abd2fa696c53769f43580aea78ae97a19912@group.calendar.google.com", line="SXR", machine="SC", hutch="qRIXS", is_program=True)
            ]