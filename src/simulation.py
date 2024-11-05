from .subtensor import Subtensor
import importlib
import re
from .plotting import BasePlot
from typing import Dict, Any, Optional, List, Union
import matplotlib.pyplot as plt


def parse_plot_argument(plot_arg: str) -> tuple[str, Optional[Union[List[Any], Any]]]:
    match = re.match(r'([^[]+)(?:\[(.*)\])?', plot_arg)
    if not match:
        return plot_arg, None
    
    module_name, params_str = match.groups()
    if not params_str:
        return module_name, None

    params = [param.strip() for param in params_str.split(',')]
    
    converted_params = []
    for param in params:
        try:
            converted_params.append(int(param))
        except ValueError:
            try:
                converted_params.append(float(param))
            except ValueError:
                converted_params.append(param)
    
    return module_name, converted_params[0] if len(converted_params) == 1 else converted_params


def run_simulation(config: Dict[str, Any], plot_modules: Optional[List[str]] = None):
    blocks = config['blocks']
    n_steps = config['n_steps']
    subnets = config['subnets']
    accounts = config['accounts']
    trades = config['trades']
    tao_supply = config['tao_supply']
    global_split = config['global_split']
    balanced = config['balanced']
    root_weight = config['root_weight']

    subtensor = Subtensor(
        subnets=subnets,
        accounts=accounts,
        trades=trades,
        tao_supply=tao_supply,
        global_split=global_split,
        balanced=balanced,
        root_weight=root_weight,
        blocks=blocks,
        n_steps=n_steps
    )

    subtensor.run_simulation()

    if plot_modules:
        plotters = []
        for plot_arg in plot_modules:
            try:
                module_name, params = parse_plot_argument(plot_arg)
                
                module = importlib.import_module(module_name)
                
                plot_class = [obj for obj in module.__dict__.values() 
                             if isinstance(obj, type) and issubclass(obj, BasePlot) 
                             and obj != BasePlot][-1]
                
                plotter = plot_class("data", config["blocks"], config["n_steps"])
                
                if params is not None:
                    plotter.plot(params)
                else:
                    plotter.plot()
                    
                plotters.append(plotter)
                
            except Exception as e:
                print(f"Error running plot {plot_arg}: {str(e)}")

        plt.show()
