# Accounting Exchange reports

The [structured report details](accounting-exchange.json) give the controls, return layouts, source locations and available procedure identifiers. See the [reading guide](README.md) for how settings select a result.

## DATEV

Script Report. The reference record is GL Entry. Declared inputs include `company`, `from_date`, `to_date`, `voucher_type`.

The direct return positions are COLUMNS / data. [Row procedure](https://github.com/alyf-de/erpnext_datev/blob/2757764727bb162f5aecaf990fc0479e819c20f8/erpnext_datev/erpnext_datev/report/datev/datev.py#L154) [Declaration](https://github.com/alyf-de/erpnext_datev/blob/2757764727bb162f5aecaf990fc0479e819c20f8/erpnext_datev/erpnext_datev/report/datev/datev.json) [Module bindings](procedures/accounting-exchange--datev-bindings.json) · [Ordered report procedures](procedures/accounting-exchange--datev-1.json)
