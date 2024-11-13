library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity LED_Controller_AXI_tb is
end LED_Controller_AXI_tb;

architecture Behavioral of LED_Controller_AXI_tb is
    -- Component declaration of the DUT (Device Under Test)
    component LED_Controller_AXI
        Port (
            -- AXI Signals
            S_AXI_ACLK      : in std_logic;
            S_AXI_ARESETN   : in std_logic;
            S_AXI_AWADDR    : in std_logic_vector(3 downto 0);
            S_AXI_AWVALID   : in std_logic;
            S_AXI_WDATA     : in std_logic_vector(31 downto 0);
            S_AXI_WVALID    : in std_logic;
            S_AXI_BREADY    : in std_logic;
            S_AXI_ARADDR    : in std_logic_vector(3 downto 0);
            S_AXI_ARVALID   : in std_logic;
            S_AXI_RREADY    : in std_logic;
            S_AXI_BVALID    : out std_logic;
            S_AXI_RVALID    : out std_logic;
            S_AXI_RDATA     : out std_logic_vector(31 downto 0);
            S_AXI_WREADY    : out std_logic;
            S_AXI_AWREADY   : out std_logic;
            S_AXI_ARREADY   : out std_logic;

            -- LED Control Signals
            clk             : in std_logic;
            reset           : in std_logic;
            led_out         : out std_logic
        );
    end component;

    -- Testbench signals
    signal S_AXI_ACLK      : std_logic := '0';
    signal S_AXI_ARESETN   : std_logic := '0';
    signal S_AXI_AWADDR    : std_logic_vector(3 downto 0) := (others => '0');
    signal S_AXI_AWVALID   : std_logic := '0';
    signal S_AXI_WDATA     : std_logic_vector(31 downto 0) := (others => '0');
    signal S_AXI_WVALID    : std_logic := '0';
    signal S_AXI_BREADY    : std_logic := '1';
    signal S_AXI_ARADDR    : std_logic_vector(3 downto 0) := (others => '0');
    signal S_AXI_ARVALID   : std_logic := '0';
    signal S_AXI_RREADY    : std_logic := '1';
    signal S_AXI_BVALID    : std_logic;
    signal S_AXI_RVALID    : std_logic;
    signal S_AXI_RDATA     : std_logic_vector(31 downto 0);
    signal S_AXI_WREADY    : std_logic;
    signal S_AXI_AWREADY   : std_logic;
    signal S_AXI_ARREADY   : std_logic;

    signal clk             : std_logic := '0';
    signal reset           : std_logic := '0';
    signal led_out         : std_logic;

    -- Clock generation process
    constant CLOCK_PERIOD : time := 10 ns;
begin
    -- Instantiate the DUT
    DUT: LED_Controller_AXI
        Port map (
            S_AXI_ACLK      => S_AXI_ACLK,
            S_AXI_ARESETN   => S_AXI_ARESETN,
            S_AXI_AWADDR    => S_AXI_AWADDR,
            S_AXI_AWVALID   => S_AXI_AWVALID,
            S_AXI_WDATA     => S_AXI_WDATA,
            S_AXI_WVALID    => S_AXI_WVALID,
            S_AXI_BREADY    => S_AXI_BREADY,
            S_AXI_ARADDR    => S_AXI_ARADDR,
            S_AXI_ARVALID   => S_AXI_ARVALID,
            S_AXI_RREADY    => S_AXI_RREADY,
            S_AXI_BVALID    => S_AXI_BVALID,
            S_AXI_RVALID    => S_AXI_RVALID,
            S_AXI_RDATA     => S_AXI_RDATA,
            S_AXI_WREADY    => S_AXI_WREADY,
            S_AXI_AWREADY   => S_AXI_AWREADY,
            S_AXI_ARREADY   => S_AXI_ARREADY,
            clk             => clk,
            reset           => reset,
            led_out         => led_out
        );

    -- Clock generation
    clk_process: process
    begin
        while true loop
            S_AXI_ACLK <= '0';
            clk <= '0';
            wait for CLOCK_PERIOD / 2;
            S_AXI_ACLK <= '1';
            clk <= '1';
            wait for CLOCK_PERIOD / 2;
        end loop;
    end process;

    -- Test stimulus
    stimulus: process
    begin
        -- Apply reset
        reset <= '1';
        S_AXI_ARESETN <= '0';
        wait for 20 ns;
        reset <= '0';
        S_AXI_ARESETN <= '1';

        -- Wait for reset to propagate
        wait for 20 ns;

        -- Send a command to turn on the LED with full brightness
        S_AXI_AWADDR <= "0000";
        S_AXI_AWVALID <= '1';
        S_AXI_WDATA <= X"00000001"; -- Command to turn LED ON at full brightness
        S_AXI_WVALID <= '1';
        wait for CLOCK_PERIOD;

        -- Wait for the AXI transaction to complete
        wait until S_AXI_AWREADY = '1' and S_AXI_WREADY = '1';
        S_AXI_AWVALID <= '0';
        S_AXI_WVALID <= '0';
        wait for CLOCK_PERIOD;

        -- Check if the LED is turned on
        assert led_out = '1' report "LED did not turn ON as expected" severity error;

        -- Finish simulation
        wait for 50 ns;
        report "Testbench completed successfully!" severity note;
        wait;
    end process;
end Behavioral;
