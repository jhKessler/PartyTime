import {Component} from '@angular/core';
import {StatsService} from "../stats.service";
import * as moment from 'moment'

import {ChartOptions, ChartType} from 'chart.js';
import {Label} from 'ng2-charts';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent {

  public barChartOptions: ChartOptions = {
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
      display: false
    },
    defaultColor: 'red'
  };
  public barChartLabels: Label[] = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'];
  public barChartType: ChartType = 'bar';

  constructor(public statsService: StatsService) {
  }

  daysLeft(date: Date) {
    return moment(date).diff(moment(), 'days');
  }

}
