from ..commands.portfolioOpt import sharpe

def stat_process(action, event):
  if action == 'PORTFOLIO_OPT':
    return sharpe.process(event)