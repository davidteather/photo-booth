interface PhotoResponse {
  photo_id: string;
}

interface SendPhotoRequest {
  photo_ids: string[];
  emails: string[];
  phones: string[];
  promotional_consent: boolean;
}

interface SendPhotoResponse {
  success: boolean;
}

class APIService {
  private baseUrl: string = import.meta.env.PUBLIC_API_URL || "";
  private password: string = import.meta.env.PUBLIC_APP_PASSWORD || "";

  public getStreamUrl(): string {
    return this.addURLToken(`${this.baseUrl}/stream`);
  }

  private addURLToken(url: string): string {
    return `${url}?password=${this.password}`;
  }

  public async takePhoto(): Promise<PhotoResponse> {
    const response = await fetch(this.addURLToken(`${this.baseUrl}/capture`), {
      method: "POST",
    });
    return response.json() as Promise<PhotoResponse>;
  }

  public async getPhoto(photo_id: string): Promise<string> {
    const response = await fetch(
      this.addURLToken(`${this.baseUrl}/photos/${photo_id}`)
    );
    const blob = await response.blob();
    return URL.createObjectURL(blob);
  }

  public async sendPhoto(
    request: SendPhotoRequest
  ): Promise<SendPhotoResponse> {
    const response = await fetch(this.addURLToken(`${this.baseUrl}/send`), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
    return response.json() as Promise<SendPhotoResponse>;
  }
}

export default new APIService();
