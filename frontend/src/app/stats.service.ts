import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {DataModel} from "./data.model";

@Injectable({
  providedIn: 'root'
})
export class StatsService {

  data: DataModel

  constructor(private http: HttpClient) {
    this.updateData()
  }

  updateData() {
    this.http.get<DataModel>('/data').subscribe(res => this.data = res);
  }
}
