import datetime
from enum import Enum, IntEnum
from dataclasses import dataclass, field
from typing import Optional, List, Callable, Tuple, Dict, Any

# ==================== Enums ====================

class ConnectionType(Enum):
    BLE = 0

class EarSide(IntEnum):
    Left = 0x00
    Right = 0x01

class SignalQuality(Enum):
    OK = 0
    SizeError = 1
    OriginalMaxValue = 2
    OriginalZeroValue = 3
    FilteredMaxValue = 4
    FilteredZeroValue = 5
    ThresholdError = 6
    PowerFrequencyError = 7
    OtherError = 8

# ==================== Data Models ====================

@dataclass
class BleDeviceInfo:
    Id: str
    Name: str
    BluetoothAddress: int
    IsConnected: bool = False

@dataclass
class DeviceStateEventArgs:
    ConnectionType: ConnectionType
    IsConnected: bool
    Message: Optional[str] = None

@dataclass
class DeviceStatusNotificationEventArgs:
    Command: int
    EarSide: int
    LeftBattery: int
    RightBattery: int
    LeftWorn: bool
    RightWorn: bool
    HardwareVersion: int
    SoftwareVersion: int
    IsBigEndian: bool
    NoiseReductionMode: int
    TouchEnabled: bool
    AutoPlayStopEnabled: bool
    IsValid: bool
    ErrorMessage: Optional[str] = None
    Timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class DataReceivedEventArgs:
    EarSide: EarSide
    Data: List[float]
    PacketCounter: int
    IsValid: bool
    ErrorMessage: Optional[str] = None
    Timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class SpectrumDataEventArgs:
    LeftDelta: float
    LeftTheta: float
    LeftAlpha: float
    LeftBeta: float
    LeftGamma: float
    LeftLowAlpha: float
    LeftHighAlpha: float
    LeftLowBeta: float
    LeftHighBeta: float
    LeftLowGamma: float
    LeftHighGamma: float
    RightDelta: float
    RightTheta: float
    RightAlpha: float
    RightBeta: float
    RightGamma: float
    RightLowAlpha: float
    RightHighAlpha: float
    RightLowBeta: float
    RightHighBeta: float
    RightLowGamma: float
    RightHighGamma: float
    LeftSignalQuality: SignalQuality
    RightSignalQuality: SignalQuality
    Timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class MentalStateDataEventArgs:
    Focus: float
    Fatigue: float
    Relax: float
    Calm: float
    Stress: float
    Timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class ServerAuthResultEventArgs:
    IsSuccess: bool
    Permission: str
    Timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    BoundAt: Optional[str] = None
    LastSeen: Optional[str] = None
    ErrorMessage: Optional[str] = None

# ==================== Core SDK ====================

class NaoyunSdkApi:
    IsConnected: bool

    # Callbacks
    BleDeviceDiscovered: Optional[Callable[[BleDeviceInfo], None]]
    ConnectionStateChanged: Optional[Callable[[DeviceStateEventArgs], None]]
    DeviceStatusNotificationReceived: Optional[Callable[[DeviceStatusNotificationEventArgs], None]]
    DataReceived: Optional[Callable[[DataReceivedEventArgs], None]]
    SpectrumDataReceived: Optional[Callable[[SpectrumDataEventArgs], None]]
    SpectrumTaskStatusChanged: Optional[Callable[[bool, str], None]]
    MentalStateDataReceived: Optional[Callable[[MentalStateDataEventArgs], None]]
    ServerAuthCompleted: Optional[Callable[[ServerAuthResultEventArgs], None]]
    on_log_message: Optional[Callable[[str], None]]

    def __init__(self) -> None: ...

    # Initialization & Version
    def Initialize(self, app_id: str, app_secret: str, is_domestic: bool = True) -> None: ...
    def GetSdkVersion(self) -> str: ...

    # BLE Scan
    async def StartBleScanAsync(self, timeout: datetime.timedelta) -> List[BleDeviceInfo]: ...
    async def StopBleScanAsync(self) -> None: ...

    # Connection
    async def ConnectBleAsync(self, bluetooth_address: str) -> bool: ...
    async def DisconnectAsync(self) -> None: ...

    # Data Control
    async def SendStartDataAsync(self) -> bool: ...
    async def SendStopDataAsync(self) -> bool: ...
    async def SendInitCommandAsync(self) -> bool: ...
    async def GetMacAddressAsync(self) -> bool: ...

    # Device Status Control
    async def SetNoiseReductionModeAsync(self, mode: int) -> Tuple[bool, bool]: ...
    async def SetTouchEnabledAsync(self, enabled: bool) -> Tuple[bool, bool]: ...
    async def SetAutoPlayEnabledAsync(self, enabled: bool) -> Tuple[bool, bool]: ...

    # Data Retrieval
    def GetLatestEegData(
        self, ear_side: EarSide, seconds: int, use_filtered_data: bool = False
    ) -> List[float]: ...
    def get_current_status(self) -> Dict[str, Any]: ...

    # Properties
    @property
    def MacAddress(self) -> Optional[str]: ...

    # Algorithm Tasks
    def StartSpectrumTask(self) -> bool: ...
    def StopSpectrumTask(self) -> None: ...
    def StartMentalStateTask(self, interval_seconds: float = 1.0) -> bool: ...
    def StopMentalStateTask(self) -> None: ...

# ==================== Helpers ====================

def save_eeg_to_excel(
    left_data: List[float],
    right_data: List[float],
    filename: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str: ...
