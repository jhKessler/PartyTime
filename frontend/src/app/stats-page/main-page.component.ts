import {Component} from '@angular/core';
import {StatsService} from "../stats.service";
import {ChartOptions, ChartType} from "chart.js";
import * as moment from "moment";

@Component({
  selector: 'app-stats-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent {

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

  constructor(public statsService: StatsService) {
  }


  daysLeft(date: Date) {
    return moment(date).diff(moment(), 'days');
  }

}
