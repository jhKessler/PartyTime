import { Component, OnInit } from '@angular/core';
import {StatsService} from "../stats.service";

@Component({
  selector: 'app-stats-page',
  templateUrl: './stats-page.component.html',
  styleUrls: ['./stats-page.component.scss']
})
export class StatsPageComponent implements OnInit {

  constructor(public statsService: StatsService) { }

  ngOnInit(): void {
  }

}
