export interface DataModel {
  last_seven_days_total: number,
  last_seven_days_avg: number,
  einwohner_deutschland: number,
  impfrate_herdenimmunitaet: number,
  menschen_fuer_herdenimmunitaet: number,
  dosen_fuer_herdenimmunitaet: number,
  impfdosen_bisher: number,
  impfdosen_uebrig: number,
  genug_leute_geimpft: Date,
  impfungen_nach_wochentag_avg: number[],
  stand: Date
}
