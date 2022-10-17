from .portfolioOpt import efficientFrontier

def stat_process(action, event):
  if action == 'PORTFOLIO_OPT':
    return efficientFrontier.process(event)