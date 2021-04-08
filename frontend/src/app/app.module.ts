import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {MainPageComponent} from './main-page/main-page.component';
import {RouterModule} from '@angular/router';
import {StatsPageComponent} from './stats-page/stats-page.component';
import {MomentModule} from 'ngx-moment';
import {ChartsModule} from 'ng2-charts';
import {HttpClientModule} from "@angular/common/http";

@NgModule({
  declarations: [
    AppComponent,
    MainPageComponent,
    StatsPageComponent
  ],
  imports: [
    BrowserModule,
    MomentModule,
    ChartsModule,
    HttpClientModule,
    RouterModule.forRoot([
      {
        path: '',
        pathMatch: 'full',
        component: MainPageComponent
      },
      {
        path: 'stats',
        component: StatsPageComponent
      }
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
