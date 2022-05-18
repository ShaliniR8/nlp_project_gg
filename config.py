from configparser import ConfigParser

def run():
    #configparser object
    cf = ConfigParser()

    #Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
    cf["CEREMONY"] = {
        "name1": "Golden Globes",
        "name2": "Golden Globe"
    } # should we include info like attendents: "actor", "actress", topic: "award"??

    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        cf.write(conf)

if __name__ == "__main__": run()