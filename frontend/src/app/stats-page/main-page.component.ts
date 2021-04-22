import {AfterViewInit, Component, OnInit} from '@angular/core';
import {StatsService} from "../stats.service";
import {ChartOptions, ChartType} from "chart.js";
import * as moment from "moment";
import * as HRN from 'human-readable-numbers'

@Component({
  selector: 'app-stats-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements OnInit {

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
          fontColor: 'rgb(210,210,210)',
          callback(value: number | string, index: number, values: number[] | string[]): string | number | null | undefined {
            return HRN.toHumanString(value);
          }
        }
      }]
    },
    legend: {
      display: true,
      labels: {
        fontColor: 'white'
      }
    },
    tooltips: {
      callbacks: {
        afterLabel(tooltipItem: Chart.ChartTooltipItem, data: Chart.ChartData): string | string[] {
          return [
            'Formatiert: ' + HRN.toHumanString(tooltipItem.value)
          ];
        }
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

  ngOnInit() {
    this.lineChartOptions.tooltips.callbacks.title = ((item, data) => {
      return this.statsService.data.week_start_end[item[0].index];
    });
  }

}
