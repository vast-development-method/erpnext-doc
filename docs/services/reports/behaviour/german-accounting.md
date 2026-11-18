# German Accounting reports

The [structured report details](german-accounting.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## Summen- und Saldenliste

Script Report. The reference record is GL Entry. Declared inputs include `company`, `fiscal_year`, `month`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `account`, `account_currency`, `debit_opening_balance`, `credit_opening_balance`, `debit_until_evaluation_period`, `credit_until_evaluation_period`, `debit_in_evaluation_period`, `credit_in_evaluation_period`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/alyf-de/erpnext_germany/blob/9df60071fe8fc8f65a0b927b5d095476f7882f36/erpnext_germany/erpnext_germany/report/summen__und_saldenliste/summen__und_saldenliste.py#L14) [Declaration](https://github.com/alyf-de/erpnext_germany/blob/9df60071fe8fc8f65a0b927b5d095476f7882f36/erpnext_germany/erpnext_germany/report/summen__und_saldenliste/summen__und_saldenliste.json) [Module bindings](procedures/german-accounting--summen-und-saldenliste-bindings.json) · [Ordered report procedures](procedures/german-accounting--summen-und-saldenliste-1.json)

## Zusammenfassende Meldung

Script Report. The reference record is Sales Invoice. Declared inputs include `company`, `year`, `period`.

The direct return positions are get columns / get data. Named output fields constructed in this report include `tax_id`, `amount`, `service_type`. The structured entry gives their enclosing conditions and builders. [Row procedure](https://github.com/alyf-de/erpnext_germany/blob/9df60071fe8fc8f65a0b927b5d095476f7882f36/erpnext_germany/erpnext_germany/report/zusammenfassende_meldung/zusammenfassende_meldung.py#L41) [Declaration](https://github.com/alyf-de/erpnext_germany/blob/9df60071fe8fc8f65a0b927b5d095476f7882f36/erpnext_germany/erpnext_germany/report/zusammenfassende_meldung/zusammenfassende_meldung.json) [Module bindings](procedures/german-accounting--zusammenfassende-meldung-bindings.json) · [Ordered report procedures](procedures/german-accounting--zusammenfassende-meldung-1.json)
