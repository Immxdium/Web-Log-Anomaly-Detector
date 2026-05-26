import type { AnalyzeResponse } from '@/types';
import axios from 'axios';

const client = axios.create({ baseURL: '/api' })

export const api = {
    health: () => client.get('/health'),

    analyze: (file: File): Promise<AnalyzeResponse> => {
        const form = new FormData()
        form.append('file', file)
        return client
          .post<AnalyzeResponse>('/analyze', form, {
            headers: { 'Content-Type': 'multipart/form-data' },
          })
          .then((r) => r.data)
    }
}