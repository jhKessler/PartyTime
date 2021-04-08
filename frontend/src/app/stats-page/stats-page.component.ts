import { Component, OnInit } from '@angular/core';
import {StatsService} from "../stats.service";
import {ChartOptions, ChartType} from "chart.js";
import {Label} from "ng2-charts";

@Component({
  selector: 'app-stats-page',
  templateUrl: './stats-page.component.html',
  styleUrls: ['./stats-page.component.scss']
})
export class StatsPageComponent implements OnInit {

  public lineChartOptions: ChartOptions = {
    responsive: true,
    scales: {
      xAxes: [{
        gridLines: {display: false},
        ticks: {
          fontColor: 'rgb(210,210,210)'
        }
      }],
      yAxes: [{
        gridLines: {display: false},
        ticks: {
          min: 0,
          fontColor: 'rgb(210,210,210)'
        }
      }]
    },
    legend: {
      display: true,
      labels: {
        fontColor: 'white'
      }
    },
    defaultColor: 'red'
  };
  public lineChartType: ChartType = 'line';

  constructor(public statsService: StatsService) { }

  ngOnInit(): void {
  }

}
