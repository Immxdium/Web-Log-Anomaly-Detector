export interface Summary {
    total_requests: number;
    unique_ips:     number;
    high_alerts:    number;
    medium_alerts:  number;
}

export interface Detection {
    [key: string]: string | number
}

export interface Detection {
    key:    string;
    title:  string;
    severity: 'HIGH' | 'MEDIUM' | 'LOW'
    count:  number
    columns: string[]
    data:   DetectionRow[]
}

export interface AnalyzeResponse {
    summary: Summary;
    detections: Detection[]
}